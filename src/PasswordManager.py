import hashlib
import base64


class PWDManager():
  
   IsValid = False
  
  def __init__(self, master_password):
    print('[*] Password Manager Has Been Loaded!')
    if master_password == '1':
      self.IsValid = True
    else:
      self.IsValid = False
