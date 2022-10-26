### To deploy Kudos user event script

#### Workplace side:

1. Create a group for Kudos and note down group id (can get from group URL)
2. Create Integration under Admin Panel -> Integrations 
3. Generate a token for created Integration and note it to a secure place
(**destroy the noted token afterwards**)

#### NetSuite side:

1. Upload code to a FileCabinet
2. Create API secret in Setup -> Company -> API Secrets <br>
	2.1. Parameters: <br> 
	name = 'wp_access_token' <br>
	id = 'wp_access_token' <br>
	password = token for Workplace Integration (item #2).
3. Create Integration Mapping under Setup -> Integration -> Integration Mapping and note its id <br>
	Parameters: <br> 
	URL = 'https://graph.facebook.com/v14.0/' <br>
	Secret Key = '{custsecretwp\_access\_token}'
4. Create a new script record out of UserEvent script (postkudos.js)
5. Create parameters for a script record <br>
	5.1. Label = '\_mapid', id = '\_mapid', type = 'Integer Number' <br>
	5.2. Label = '\_groupid', id = '_groupid', type = 'Integer Number'
6. Create a Script Deployment and fill in parameters with values for group id and integration mapping id. 