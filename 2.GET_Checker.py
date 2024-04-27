from burp import IBurpExtender, IHttpListener, IHttpRequestResponse

# Based on: https://github.com/PortSwigger/filter-options-method/blob/master/filter-options-method.py

class BurpExtender(IBurpExtender, IHttpListener, IHttpRequestResponse):
    # Define the BurpExtender class implementing IBurpExtender and IHttpListener interfaces.
  
  def registerExtenderCallbacks(self, callbacks):
    # Method to register extension callbacks.
    self._callbacks = callbacks
    self._helpers = callbacks.getHelpers()
    callbacks.registerHttpListener(self)
    callbacks.setExtensionName("GET Checker")
    print("Loading Extension 2")
  
  def processHttpMessage(self, tool, is_request, content):
    # Method to process an HTTP message (either request or response).
    if not is_request:
      # If the petition is not a request, return.
      return
    requestBytes = content.getRequest()
    requestInfo = self._helpers.analyzeRequest(content.getHttpService(), requestBytes)
    if requestInfo.getMethod() == "POST":
      # Only apply the procedure if the method is "POST".
      headers = requestInfo.getHeaders()
      # Find Content-Type header.
      content_type_header = [header for header in headers if header.startswith("Content-Type")]
      if content_type_header:
        content_type = content_type_header[0].split(": ")[1]
        print("Content-Type:", content_type)
        if content_type == "application/x-www-form-urlencoded":
          # Only applies if the request is Content-Type: application/x-www-form-urlencoded.
          print("Content-Type is application/x-www-form-urlencoded")
          cur_request_info = self._helpers.analyzeRequest(content)
          bodyRequestString = requestBytes[cur_request_info.getBodyOffset():].tostring()
          
          # Replaces the POST with a GET and adds the body as a QueryString.
          cur_request_info.getHeaders()[0] = cur_request_info.getHeaders()[0].replace("POST", "GET")
          cur_request_info.getHeaders()[0] = cur_request_info.getHeaders()[0].replace(" HTTP", "?" + bodyRequestString + " HTTP")
          new_headers = [header for header in cur_request_info.getHeaders() if not header.startswith("Content-")]
          new_message = self._helpers.buildHttpMessage(new_headers, None)
          
          # Sets the new request and obtains the response.
          content.setRequest(new_message)
          newrequestInfo = self._helpers.analyzeRequest(content.getHttpService(), new_message)
          newresponse_bytes = self._callbacks.makeHttpRequest(newrequestInfo.getUrl().getHost(), newrequestInfo.getUrl().getPort(), newrequestInfo.getUrl().getProtocol() == "https", new_message)
          newresponseInfo = self._helpers.analyzeResponse(newresponse_bytes)
          
          # If the response is 20X, then print out the request and the response.
          if 200 <= newresponseInfo.getStatusCode() < 300:
              print("----------SUCCESSFUL-RESPONSE--------------")
              print("----------REQUEST--------------")
              print(newrequestInfo.getHeaders())
              print("----------RESPONSE--------------")
              print(newresponseInfo.getHeaders())
              # Send the petitions to Repeater for careful analysis.
              self._callbacks.sendToRepeater(newrequestInfo.getUrl().getHost(), newrequestInfo.getUrl().getPort(), newrequestInfo.getUrl().getProtocol() == "https", new_message, None)
 
          return
        else:
            print("Content-Type is not application/x-www-form-urlencoded")
