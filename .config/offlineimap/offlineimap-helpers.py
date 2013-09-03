import os
import subprocess

""" Use gpg to decrypt password.
"""
def mailpasswd(path):
    cmd = "gpg --quiet --batch --use-agent --decrypt --output - " + os.path.expanduser(path)
    try:
        return subprocess.check_output(cmd, shell=True).strip()
    except subprocess.CalledProcessError:
        return ""


# mapping for nametrans
# dictionary of strings {<remote>: <local>, ...} shape, where <remote> is mapped to <local>

mapping_gmail = {
    'INBOX'                : 'INBOX',
    '[Gmail]/Drafts'       : 'drafts',
    '[Gmail]/Sent Mail'    : 'sent',
    '[Gmail]/Bin'          : 'trash',
    '[Gmail]/Spam'         : 'spam',
    'arch'                 : 'arch',
    'aur-general'          : 'aur-general',
    'arch-general'         : 'arch-general',
    'arch-wiki'            : 'arch-wiki',
}

mapping_fjfi = {
    'INBOX'                : 'INBOX',
    'Drafts'               : 'drafts',
    'Sent Items'           : 'sent',
    'Deleted Items'        : 'trash',
    'Junk E-Mail'          : 'spam',
}


# values from mapping_* dicts with high priority
prio_queue_gmail = ['INBOX', 'arch', 'arch-wiki', 'arch-general', 'aur-general']
prio_queue_fjfi = ['INBOX']


def nt_remote(mapping):
    def inner(folder):
        try:
            return mapping[folder]
        except:
            return folder
    return inner

def nt_local(mapping):
    r_mapping = dict(zip(mapping.values(), mapping.keys()))
    def inner(folder):
        try:
            return r_mapping[folder]
        except:
            return folder
    return inner


# return False if folder not in mapping.keys()
def exclude(mapping):
    def inner(folder):
        if folder in mapping.keys():
            return True
        return False
    return inner


# compare by position in queue (mapping_*.values())
def fd_priority(prio_queue):
    def inner(x, y):
        if x in prio_queue and y in prio_queue:
            return cmp(prio_queue.index(x), prio_queue.index(y))
        elif x in prio_queue:
            return -1
        elif y in prio_queue:
            return 1
        else:
            return 0
    return inner