# cylog

Python username and password encrypted cache mechanism.
Uses cryptography.fernet.Fernet() for encryption.

Examples:

    	Cylog('https://e4ftl01.cr.usgs.gov/').login()
    
This will either read the username and password from your cylog file
(default `~/.cylog/.cylog.npz`) or prompt you for these. 

Note that you may need to decode the returned binary strings, e.g.:

	uinfo = Cylog('https://e4ftl01.cr.usgs.gov/').login()
        username,password = uinfo[0].decode('utf-8'),uinfo[1].decode('utf-8') 

NAME
    cylog - # -*- coding: utf-8 -*-

PACKAGE CONTENTS


CLASSES
    builtins.object
        Cylog
    
    class Cylog(builtins.object)
     |  Cylog(site, init=False, stderr=False, verbose=False, destination_folder='.cylog')
     |  
     |  cylog provides a mechanism to partially hide username and
     |  password information that is required in plain text.
     |  
     |  It does this by storing a key and the encrypted version in
     |  a file accessible only to the user.
     |  
     |  Of course, when called (by the user) the (username, password)
     |  are exposed in plain text, so only use this when you 
     |  have to enter plain text username/password information.
     |  
     |  It is written as a utility to allow UCL MSc students to 
     |  show access to NASA Earthdata dataset download, without 
     |  the need to expose (username, password) in a submitted report.
     |  
     |  Stores (in a dictionary in ~/{dest_path}/.cylog.npz) an
     |  encrypted form of username and password (and key)
     |  
     |  Uses cryptography.fernet.Fernet() for encryption
     |  
     |  cylog().login() : returns plain text tuple
     |                    (username, password)
     |  
     |  Methods defined here:
     |  
     |  __init__(self, site, init=False, stderr=False, verbose=False, destination_folder='.cylog')
     |      Positional arguments:
     |      ----------
     |      site: 
     |         string of anchor URL for site to associate with username and
     |         password OR list of sites
     |      
     |      Keyword arguments 
     |      ----------
     |      init: bool
     |          to re-initialise the passord/username
     |          set to True. This will overwrite any existing password file.
     |      
     |      destination_folder: str
     |          The destination sub-folder, relative to ${HOME}.
     |          If this doesnt exist, it is created.
     |      
     |      verbose: Bool
     |          verbose True or False (False default)
     |      
     |      when prompted, please supply:
     |      
     |      username: str
     |          username
     |      password: str
     |          password
     |  
     |  login(self, site=None, force=False)
     |      Reads encrypted information from ~/{dest_path}/.cylog.npz
     |      
     |      Keyword arguments
     |      ----------
     |      site = False (so self.site is default)
     |             string of anchor URL for site to associate with username and
     |             password
     |      force = False
     |             force password re-entry for site
     |      
     |      Returns
     |      --------
     |      A tuple containing plain text (username,password) for (site or self.site)
     |  
     |  msg(self, *args)
     |      message passing
     |  
     |  sort_list(self, site)
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)


DATA
    __copyright__ = 'Copyright 2018 P Lewis'
    __email__ = 'p.lewis@ucl.ac.uk'
    __license__ = 'GPLv3'

AUTHOR
    P Lewis


