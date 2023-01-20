''' You work at a company that receives daily data files from external partners. These files need to be processed and analyzed, but first, they need to be transferred to the company's internal network.

The goal of this project is to automate the process of transferring the files from an external FTP server to the company's internal network.

Here are the steps you can take to automate this process:

    Use the ftplib library to connect to the external FTP server and list the files in the directory.

    Use the os library to check for the existence of a local directory where the files will be stored.

    Use a for loop to iterate through the files on the FTP server and download them to the local directory using the ftplib.retrbinary() method.

    Use the shutil library to move the files from the local directory to the internal network.

    Use the schedule library to schedule the script to run daily at a specific time.

    You can also set up a log file to keep track of the files that have been transferred and any errors that may have occurred during the transfer process. '''


from ftplib import FTP

host = "ftp.dlptest.com"
user = "dlpuser"
password = "rNrKYTX9g7z3RgJRmxWuGHbeu"  #should be taken from an external file, preferably encrypted

src_dir = ""
dest_dir = "somedir/someotherdir"

ftp = FTP(host, user=user, passwd=password)
if src_dir != "":
    ftp.cwd(src_dir)

if dest_dir != "":
    #check existence of folder(s) create if necessary and move to it
    pass
#get the files list
#files = ftp.mlsd()
files = []
ftp.retrlines('NLST', files.append)
print(files)

for file in files:
    #check existence
    #log
    with open(file, 'wb') as fp:
        ftp.retrbinary('RETR {}'.format(file), fp.write)
    #break

ftp.quit()
