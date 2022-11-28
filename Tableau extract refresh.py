import tableauserverclient as TSC

server_name = "<XX_YY>.online.tableau.com"    # Name or IP address of your installation of Tableau Server
site_url_id = "<XX_YY>"    			# Site (subpath) to sign in to. An empty string is used to specify the default site.

# For Personal Access Token sign in
personal_access_token_name = "<XX_YY>"        # Name of the personal access token.
personal_access_token_secret = "<XX_YY>"   	# Value of the token.

# Data source name for extract refresh
ds_name = '<XX_YY>'

tableau_auth = TSC.PersonalAccessTokenAuth(personal_access_token_name, 
				           personal_access_token_secret,
				           site_url_id)


server = TSC.Server(server_name, use_server_version=True)

server.auth.sign_in(tableau_auth)


with server.auth.sign_in(tableau_auth):
    all_datasources, pagination_item = server.datasources.get()

    for ds in all_datasources:
    	if ds.name == ds_name:
    		print(f"Found ds: {ds_name}, ID: {ds.id}")
    		ds_id = ds.id

    		ds_to_update = server.datasources.get_by_id(ds_id)
    		refreshed_ds = server.datasources.refresh(ds_to_update)
    		print(f"Sent DS refresh extract now")
                            break


