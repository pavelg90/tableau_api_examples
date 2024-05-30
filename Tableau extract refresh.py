import tableauserverclient as TSC

server_name = "https://<XX_YY>.online.tableau.com"    # Name or IP address of your installation of Tableau Server
site_url_id = "<XX_YY>"    			# Site (subpath) to sign in to. An empty string is used to specify the default site.

# For Personal Access Token sign in
personal_access_token_name = "<XX_YY>"        # Name of the personal access token.
personal_access_token_secret = "<XX_YY>"   	# Value of the token.

tableau_auth = TSC.PersonalAccessTokenAuth(
    personal_access_token_name,
	personal_access_token_secret,
	site_url_id
)

server = TSC.Server(server_name, use_server_version=True)
server.auth.sign_in(tableau_auth)


"""
	Find DS by tag
"""
ds_tag = 'NBA'
with server.auth.sign_in(tableau_auth):
	# Get all DSs from Server
	all_datasources, pagination_item = server.datasources.get()
	while True:
		try:
			datasources, pagination_item = server.datasources.get(
				TSC.RequestOptions(
					pagenumber=pagination_item.page_number + 1
				)
			)
			all_datasources.extend(datasources)
		except:
			break

	for ds in all_datasources:
		if ds_tag in ds.tags:
			print(f"Found ds: {ds.name}, ID: {ds.id}")

			ds_to_update = server.datasources.get_by_id(ds.id)
			refreshed_ds = server.datasources.refresh(ds_to_update)
			print(f"Sent DS refresh extract now")


"""
	Find DS by Name
"""
ds_names = ['something', 'something 2']
with server.auth.sign_in(tableau_auth):
	# Get all DSs from Server
	all_datasources, pagination_item = server.datasources.get()
	while True:
		try:
			datasources, pagination_item = server.datasources.get(
				TSC.RequestOptions(
					pagenumber=pagination_item.page_number + 1
				)
			)
			all_datasources.extend(datasources)
		except:
			break

	for ds in all_datasources:
		if ds.name in ds_names:
			print(f"Found ds: {ds.name}, ID: {ds.id}")

			ds_to_update = server.datasources.get_by_id(ds.id)
			refreshed_ds = server.datasources.refresh(ds_to_update)
			print(f"Sent DS refresh extract now")


