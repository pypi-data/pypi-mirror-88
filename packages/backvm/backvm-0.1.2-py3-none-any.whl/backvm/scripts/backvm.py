
# Author: Pietro Marini <backvm@fastmail.com>
# License: BSD 3 clause

import sys

import os

import getpass

import libvirt

import subprocess

from paramiko import SSHClient

from paramiko import WarningPolicy

from datetime import datetime

import smtplib

import ssl

from email.mime.multipart import MIMEMultipart

from email.mime.text import MIMEText

from email.mime.application import MIMEApplication

import pandas as pd

import logging

import socket

import json

import click

from distutils.util import strtobool

from ..utils import get_disks_for_domain

from ..utils import success

from ..utils import prepare_scp




@click.command()
@click.option('--email-conf',
              'email_conf_filename',
              required=False,
              default=None,
              help='''The path of a json file that contains the email
                      configuration. If specified, it must contain a
                      root element called "email". This element
                      must then contain the following values:
                    
                      \b
                         - smtp_port
                         - smtp_server
                         - sender_email
                         - from_email
                         - sender_password
                         - receiver_email
                    
                    '''
                    ,
              show_default=True)

@click.option('--dest-server-conf',
              'dest_server_conf_filename',
              required=True,
              help='''The path of a json file that contains the server
                      configuration. This is a required parameter.
                      The json file must contain a root element
                      called "dest_server". This element must then contain
                      the following values:
                      
                      \b
                          - dest_hostname
                          - dest_username
                          - dest_folder
                    
                    ''')

@click.option('--backend-copy-utility',
              'backend_copy_utility',
              required=False,
              default='rsync',
              help='''The backend copy utility to do the remote copy. Possible
                      values are 'scp' and 'rsync'
                    '''
                    ,
              show_default=True)

@click.option('--dom-names',
              'dom_names',
              required=True,
              help='''Comma-separated list of domain names
                    ''')

@click.option( '--do-backup',
               'do_backup',
               required=False,
               default='False',
               help='''Whether the backup operation is actually done.
                      Useful when you are testing and you want to avoid
                      long waiting times. Possible values \'True\', \'False\'.
                    ''')

@click.option('--logfile',
              'logfile',
              required=False,
              default='/tmp/kvm_domains_backup.log',
              help='''The location of the log file, by default
                      /tmp/kvm_domains_backup.log
                      ''',
              show_default=True)


def perform_action(dest_server_conf_filename, email_conf_filename, dom_names,
                   do_backup, backend_copy_utility, logfile
                   ):
    '''
        This program performs the backup of one or several KVM domains
    '''
    ### Input parameters - start
    dest_server_conf = json.load(open(dest_server_conf_filename, "r"))["dest_server"]

    dest_server = dest_server_conf["dest_hostname"]

    dest_username = dest_server_conf["dest_username"]

    dest_folder = dest_server_conf["dest_folder"]

    email_conf = None
    # Initialize the email parameters, if present
    if email_conf_filename:
        email_conf =  json.load(open(email_conf_filename, "r"))["email"]

        # SMTP Server port
        smtp_port = email_conf["smtp_port"]

        # SMTP Server name
        smtp_server = email_conf["smtp_server"]

        # Sender email
        sender_email = email_conf["sender_email"]

        # From email
        from_email = email_conf["from_email"]

        # Password
        sender_password = email_conf["sender_password"]

        # Receiver email
        receiver_email = email_conf["receiver_email"]

    # Domain names list
    dom_names = dom_names.split(",")

    # Transform do_backup into a bool variable
    # https://stackoverflow.com/a/35412300
    do_backup = bool(strtobool(do_backup))

    ### Input Parameters - end

    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %I:%M:%S',
                        level=logging.DEBUG, filename=logfile, filemode='w')

    t_start_script = datetime.now()

    logging.info("backup starts: %s" % t_start_script)

    logging.info("do backup: %s" % do_backup)

    host_name = socket.gethostname()

    host_ip = socket.gethostbyname(host_name)

    dest_server_ip = socket.gethostbyname(dest_server)

    logging.info("host name: %s" % host_name)

    logging.info("host ip: %s" % host_ip)

    user_name = getpass.getuser()

    logging.info("os user name: %s" % user_name)

    logging.info("backup destination server: %s (%s)" % (dest_server, dest_server_ip))

    ## Establish the connection to the (local) libvirtd daemon
    conn = libvirt.open('qemu:///system')

    if conn == None:
        logging.info('Failed to open connection to qemu:///system', file=sys.stderr)
        sys.exit(1)

    ## Initialize report to be sent by email
    report_dict = {}

    ## Check that the remote location is accessible and writable by dest_username
    ssh = SSHClient()

    ssh.load_system_host_keys()

    ssh.set_missing_host_key_policy(WarningPolicy())
    
    ssh.connect(dest_server, username=dest_username)

    _,stdout,stderr=ssh.exec_command('touch %s/write_test_kvm_backup' % dest_folder)

    if len(stderr.read().decode())>0:
        logging.info("destination folder is not writable")
        sys.exit(1)
    else:
        _,stdout,stderr=ssh.exec_command('rm %s/write_test_kvm_backup' % dest_folder)


    ## For each domain in the initial list, do the following operations
    for dom_name in dom_names:

        logging.info("starting backup for domain %s" % dom_name)

        dom = conn.lookupByName(dom_name)

        # 1.
        #   Get the disks for the domain
        dom_xml, disks = get_disks_for_domain(dom_name, conn)

        logging.info("domain %s has the following disks" % dom_name)

        for disk in disks:
            logging.info(disk)

        # 2.
        #   If the domain is alive, create a snapshot of the domain, that is create a .snap file
        #   for each .qcow2 found in function get_disks_for_domain. The .qcow2 will
        #   not be modified until a blockcommit operation happens.
        #   It looks like there is no function in libvirt_python to do this,
        #   so that we may call 'virsh snapshot-create-as' in a subprocess.
        #   If the domain is not alive, go to next step
        dom_status = dom.isActive()

        if dom_status==1:

            dom_status_name = "active"
            
            logging.info("domain %s is active" % dom_name)

            logging.info("creating snaps - start")

            try:
            
#                output = subprocess.check_output(
#                cmnd, stderr=subprocess.STDOUT, shell=True, timeout=3,
#                universal_newlines=True)
#               
                create_snap_cmd = subprocess.check_output([ "virsh", "snapshot-create-as", "--domain",
                                              dom_name, "--name", "snap", "--disk-only",
                                              "--atomic", "--no-metadata"],
                                              stderr=subprocess.STDOUT)


            except subprocess.CalledProcessError as exc:
            
                logging.info("Status : FAIL %s, %s", exc.returncode, exc.output)
        
            else:

                logging.info("creating snaps - end with %s" % create_snap_cmd)
    
        else:
            
            dom_status_name = "inactive"

            logging.info("domain %s is not active" % dom_name)

        _, disks_snap = get_disks_for_domain(dom_name, conn)

        # 3. and 4.
        #   Copy all the .qcow files and the XML definition of the domain to the destination folder
        #   If the domain is alive, merge the .snap file for each .qcow2 found in function get_disks_for_domain. If no
        #   function is available in libvirt_python we may call 'virsh blockcommit' in a subprocess-
        #   If the domain is not alive go to next step
        if backend_copy_utility=="scp":

            # Not tested with key-based authentication
            scp = prepare_scp(dest_server, dest_username)

        for disk,snap in zip(disks,disks_snap):

            disk_size_gb = round(os.path.getsize(disk)/(1024.*1024.*1024.))

            t_backup = None

            if (do_backup):
                logging.info("copying file %s (%i GB) via %s - start" % (disk, disk_size_gb,
                      backend_copy_utility))

                t0_backup = datetime.now()

                if (backend_copy_utility=="scp"):

                    scp.put(disk, dest_folder)

                elif (backend_copy_utility=="rsync"):

                    remote_copy_cmd = subprocess.run(["rsync", "-avhW", "--progress", disk,
                                    "%s@%s:%s" % (dest_username, dest_server, dest_folder)], check=True)

                t_end_backup = datetime.now()

                t_backup = "%s" % (t_end_backup - t0_backup)

                logging.info("copying file - end with %s" % (success(remote_copy_cmd.returncode)))

                logging.info("copying file - elapsed time: %s" % (t_backup))

            if dom_status==1:
            
                logging.info("committing delta back to the main disk for %s - start" % snap)

                blkcommit_cmd = 0
                
                try:
                    blkcommit_cmd = subprocess.check_output(['virsh', 'blockcommit', dom_name, snap,
                                            		'--active', '--pivot'],
                                            		stderr=subprocess.STDOUT)
                                            
                except subprocess.CalledProcessError as exc:
                    
                    logging.info("Status : FAIL %s, %s", exc.returncode, exc.output)
                                            
                else:
                    
                    logging.info("committing delta back to the main disk - end with %s"
		          	% (blkcommit_cmd))

                logging.info("removing snap %s - start" % snap)
                
                rm_cmd = subprocess.check_output(['rm', '-f', snap],
                                                 stderr=subprocess.STDOUT)
                
                logging.info("removing snap - end with %s" % (rm_cmd))

            report_dict[disk] = {"disk_size_gb": disk_size_gb, "t_backup": t_backup, 
                                 "dom_name": dom_name, "dom_status": dom_status_name}

        if (do_backup):
            with open("/tmp/dom.xml","w") as fl:
                fl.write(dom_xml)

            logging.info("copying domain XML definition via %s - start" % backend_copy_utility)

            if backend_copy_utility == "scp":

                scp.put("/tmp/dom.xml", "%s/%s.xml" % (dest_folder,dom_name))

            elif backend_copy_utility == "rsync":

                remote_xmlcopy_cmd = subprocess.run(["rsync", "-avhW", "--progress", "/tmp/dom.xml",
                                                      "%s@%s:%s/%s.xml" % (dest_username, dest_server,
                                                     dest_folder, dom_name)], check=True)

            logging.info("copying domain XML definition - end with %s" % success(remote_xmlcopy_cmd.returncode))

    # 5.
    #   Notify with an email about the execution. The email should include, for each domain, the time spent in the
    #   backup operation, the disks size, whether the domain was live or not and other relevant information,

    report = pd.DataFrame.from_dict(report_dict, orient="index")

    report["t_backup"] = report.t_backup.astype(str)

    t_end_script = datetime.now()

    if email_conf_filename:
        # create message object instance
        msg = MIMEMultipart()

        # setup the parameters of the message
        msg['From'] = from_email

        msg['To'] = receiver_email

        msg['Subject'] = "KVM Domains Backup Report"

        # add the report to the message body
        msg.attach(MIMEText(report.to_string(), 'plain'))

        # add the summary to the message body

        summary = "backup up running on machine:".ljust(50) + "%s (%s)" % (host_name, host_ip)
        
        dry_run="True"

        if do_backup==True:
        
            dry_run="False"
        
        summary += "\ndry-run:".ljust(50) + "%s" % (dry_run)

        summary += "\nbackup destination server".ljust(50) + "%s (%s)" % (dest_server, dest_server_ip)

        summary += "\nbackup destination location".ljust(50) + "%s" % (dest_folder)

        summary += "\nnumber of backed up domains:".ljust(50) + "%i" % len(dom_names)

        summary += "\ntotal size of backed up disk:".ljust(50) + "%i GB" % report["disk_size_gb"].sum()

        summary += "\nstart time:".ljust(50) + "%s" % t_start_script

        summary += "\nend time:".ljust(50) + "%s" % t_end_script

        summary += "\ntotal execution time:".ljust(50) + "%s" % (t_end_script-t_start_script)

        msg.attach(MIMEText(summary, 'plain'))

        context = ssl.create_default_context()

    # 6.
    #   End

    logging.info("backup ends: %s" % t_end_script)

    logging.info("total elapsed time: %s" % (t_end_script-t_start_script))

    if email_conf_filename:
        ## The log file is now closed. Attach the log file and send the email
        with open(logfile, "rb") as fl:
            part = MIMEApplication(fl.read(), Name=os.path.basename(logfile))

        # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(logfile)

        msg.attach(part)


        with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
            server.login(sender_email, sender_password)

            server.sendmail(sender_email, receiver_email, msg.as_string())

