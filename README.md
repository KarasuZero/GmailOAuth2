# GmailOAuth2
an application that requests, and is granted, read access to your gmail email account using the OAuth2 protocol.  When the application is run the user can either give it access to a user's gmail account, or the user can select a gmail account that already is accessible and search for emails containing keywords.


Requirements
Your application must request access to a user's gmail account using the OAuth2 protocol supported by google and the gmail api (see resources below).
Your application should persist these OAuth settings locally
Your application must gracefully handle both the case in which access is sucessfully granted by the user, and also in the case in which the access grant fails.
Your application should maintain a list of gmail accounts to which the app has already been given access. Your application should demonstrate the ability for at least three different gmail accounts to provide OAuth authorization to your email search app.
If the user wishes to search for emails they should be required to select an already-authorized account and enter the keywords they wish to use in the search.
The application should find matches for the search keywords in the selected inbox for the logged-in gmail account and display the following info for each matching email:  sender's email address, email subject, and a count of the number of times each search term is found in the email.
