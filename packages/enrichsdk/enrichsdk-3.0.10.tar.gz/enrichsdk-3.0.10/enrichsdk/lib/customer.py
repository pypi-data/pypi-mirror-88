import os 
import sys 
import json 
import logging 

logger = logging.getLogger('app') 

def should_skip(name): 

    return (name.startswith(".") or 
            name == "__pycache__") 

def load_customer_assets(context={}): 
    """
    Go through the customer directories and add the assets from all
    installed customer modules. 

    The ENRICH_CUSTOMERS looks like system path, and it is processed 
    as such. It gives priority to the modules earlier in the path 
    than later. Typically you create a run directory and prepend
    that run directory in front of the standard directory.
    """

    assets = {} 

    # Check if the environment is correctly configured 
    enrich_customers = context.get('ENRICH_CUSTOMERS',
                                   os.environ.get('ENRICH_CUSTOMERS',
                                                  None))

    if enrich_customers is None: 
        logger.error("Customer root is missing : {}".format(enrich_customers))
        return assets

    #=> Collect all possible paths..
    customer_roots = {}
    for path in enrich_customers.split(";"):
        if not os.path.exists(path):
            continue
        for c in os.listdir(path):
            if c not in customer_roots:
                customer_roots[c] = os.path.join(path,c)

    # Now go through each of them...
    for c, customer_dir in customer_roots.items():

        # parent
        customer_root = os.path.dirname(customer_dir)

        if not os.path.isdir(customer_dir) or should_skip(c): 
            continue 

        enrichfile = os.path.join(customer_dir, 'enrich.json')
        if not os.path.exists(enrichfile): 
            logger.debug("Missing enrichfile. Skipping customer: {}".format(c))
            continue 

        try: 
            enrich = json.load(open(enrichfile)) 
        except: 
            logger.debug("Invalid enrichfile. Skipping customer: {}".format(c)) 
            
        if not enrich.get('enable', True): 
            logger.debug("Disabled customer. Skipping customer: {}".format(c)) 
            continue 
            
        for o in os.listdir(customer_dir): 
            """
            Each organization within the customer 
            """
            org_dir = os.path.join(customer_dir, o) 

            if not os.path.isdir(org_dir) or should_skip(o): 
                continue 

            enrichfile = os.path.join(org_dir, 'enrich.json')

            if not os.path.exists(enrichfile): 
                logger.debug("Missing enrichfile. Skipping org: {}:{}".format(c,o))
                continue 

            try: 
                enrich = json.load(open(enrichfile)) 
            except: 
                logger.debug("Invalid enrichfile. Skipping org: {}:{}".format(c,o)) 
            
            if not enrich.get('enable', True): 
                logger.debug("Disabled org. Skipping org: {}:{}".format(c, o)) 
                continue 

                
            # => Check assets
            # Contrib
            #        /pkg
            #            /assets
            #        /assets
            
            for assetsdir in [os.path.join(org_dir, 'pkg', 'assets'),
                              os.path.join(org_dir, 'assets')]: 
                if not os.path.exists(assetsdir): 
                    continue 
    
                for a in os.listdir(assetsdir): 
                    if should_skip(a): 
                        continue 

                    for pkgdir in [ os.path.join(assetsdir, a, a),
                                    os.path.join(assetsdir, a, 'src', a)]: 

                        if not os.path.exists(pkgdir):
                            continue
                    
                        libdir = os.path.abspath(os.path.dirname(pkgdir))
                        if libdir not in sys.path: 
                            sys.path.append(libdir)

                        assets[a] = {
                            'fullpath': os.path.join(libdir, a),
                            'relpath': os.path.relpath(os.path.join(libdir, a),
                                                       customer_root),                     
                            'organization': enrich['org']['name'],
                            'customer': c
                        }

    return assets 
