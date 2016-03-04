'''
Script to print the failing images from http://koji.fedoraproject.org/koji/tasks?state=all&view=tree&method=livecd
'''

from lxml import html
import requests
import sendgrid

def main():
    page = requests.get('http://koji.fedoraproject.org/koji/tasks?state=all&view=tree&method=livemedia')
    tree = html.fromstring(page.content)

    return tree.xpath('//a[@class="taskfailed"]')

if __name__ == '__main__':
    failed = main()
    if failed:
        message_body = '\n\n'.join([image.text for image in failed])
        sg = sendgrid.SendGridClient('API KEY') # Please get one and replace it here
        message = sendgrid.Mail()
        message.add_to('Amit Saha <amitsaha.in@gmail.com>')
        message.set_subject('Koji failed builds')
        message.set_text(message_body)
        message.set_from('Amit Saha <amitsaha.in@gmail.com>')
        status, msg = sg.send(message)
