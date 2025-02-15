import pysftp
import time
import logging
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
sendgrid_api_key = 'xxx'
logging.basicConfig(filename='sftp.log', format='%(asctime)s - %(message)s', level=logging.INFO)
logging.info('This will get logged to a file')

def send_alert_email(subject='Sftp_detector alert'):    
    ret=False
        
    sg = sendgrid.SendGridAPIClient(api_key=sendgrid_api_key)

    from_email = Email('chen@kongdigital.com')  # Change to your verified sender
    to_email = To("snsengine@gmail.com")  # Change to your recipient
    subject = 'message alert: '+subject
    content = Content("text/html", "<p>The key program:" + subject + " was NOT running just now,please check sftp 51.210.155.58</p>\
                                  <p>The Gpace Team</p>")
    try:
        mail = Mail(from_email, to_email, subject, content)

        # Get a JSON-ready representation of the Mail object
        mail_json = mail.get()

        # Send an HTTP POST request to /mail/send
        response = sg.client.mail.send.post(request_body=mail_json)
        if response.status_code==202:
            ret=True
        else:
            msg='------------------failed POST request to /mail/send in send_alert_email: '+response.text
            print(msg)
            logging.info(msg)
            
    except Exception as e:
        msg='------------------failed POST request to /mail/send in send_alert_email with Exception'
        print(msg)
        logging.info(msg)
        print(e)
        logging.info(e)
        ret = False

    print('sending email now ...' + str(ret))
    return ret


def upload_sftp_windows(input_file_path,domain='',port=22,username='',password=''):
    ret=False
   
    #pip uninstall pysftp && pip install pysftp==0.2.8
    #cnopts = pysftp.CnOpts()
    #cnopts.hostkeys = None

    #input_file_path='C:\\Users\\ychen14\\Downloads\\c++restful.txt'
    extention=input_file_path.split('.')[-1]
    try:
        with pysftp.Connection(host=domain, port=port, 
                               username=username, password=password) as sftp:
            msg='------------------Connection succesfully stablished ...'
            print(msg)
            logging.info(msg)
            
            input_file=input_file_path.split('\'')[-1]
            # Define the file that you want to upload from your local directorty
            # or absolute "C:\Users\sdkca\Desktop\TUTORIAL2.txt"
            localFilePath =input_file_path

            # Define the remote path where the file will be uploaded
            remoteFilePath = input_file.split('\\')[-1]#+'_' + datetime.datetime.now().strftime('%Y-%m-%d') + '.'+extention

            sftp.put(localFilePath, remoteFilePath)

            msg='------------------File uploaded successfully: '+localFilePath
            print(msg)
            logging.info(msg)
            ret=True
    except Exception as e:
        msg='------------------Failed to upload the file:'+input_file_path.split('\'')[-1]
        print(msg)
        logging.info(msg)
        print(e)
        logging.info(e)

        send_alert_email(msg)
        
    return ret

def test_sftp():
    input_file_path='test.txt'
    upload_sftp_windows(input_file_path)

if __name__ == "__main__":

    try:
        print("test_sftp...")
        test_sftp()
        time.sleep(600) 
    except Exception as e:
        msg="------------------test_sftp stopped."
        print(msg)
        logging.info(msg)
        logging.info(e)

