import os, requests, base64, uuid, json


endpoint = 'https://app.maximizer.ai/pubchat/api/analize'
token = os.environ['token']
project_id = os.environ['project_id']


def analize(recording_url, **kwargs):
    """
    Analize call recoring by sending POST request with data to API endpoint.

    Parameters
    ----------
    recording_url : str
        Public url or a local file path, maximum size is 10MB.
    expected_languages : list, optional
        List of languages expected to be spoken in the recording.
    project_id : str, optional
        API project_id, (default is from environment variable 'project_id').
    client_id : str, optional
        Call client_id, (default is a random UUID).
    from : str, optional
        Client name, (default is a random UUID).
    caller : str, optional
        Client phone id or number, (default is a random UUID).
    direction : str, optional
        'OUTBOUND' or 'INBOUND'.
    timestamp : str, optional
        Call start date and time, (default is to now).
    client_tasks : list, optional
        Tasks from the CRM for the given client.
    previous_calls_logs : list, optional
        Client calls before this one.
    """
    # set default values if not provided
    payload = dict(kwargs or {}, recording_url=recording_url)
    if not 'expected_languages' in payload:
      payload['expected_languages'] = ['English', 'Arabic', 'Hindi', 'Urdu']
    if not 'project_id' in payload:
      payload['project_id'] = project_id
    if not 'client_id' in payload:
      payload['client_id'] = str(uuid.uuid4())
    if not 'caller' in payload:
      payload['caller'] = str(uuid.uuid4())
    if not 'from' in payload:
      payload['from'] = str(uuid.uuid4())
    print('request payload:')
    print(payload)
    # if recording_url is not a url then read the file path
    if not recording_url.startswith('http'):
      with open(recording_url, "rb") as audio_file:
        encoded_string = 'data:audio/mp3;base64,' + base64.b64encode(
            audio_file.read()).decode("utf-8", "ignore")
      recording_url = encoded_string
      payload['recording_url'] = recording_url
    # post request with auth token
    headers = {"Authorization": "Bearer " + token}
    return requests.post(endpoint, json=payload, headers=headers)


if __name__ == '__main__':

  # example of specifying public web recording url
  # response = analize('http://fileurl...')

  # example of specifying file path recording_url
  # response = analize('call.mp3')

  # examples of specifying file path and possible languages
  # response = analize('call-cut.mp3', expected_languages=['English', 'Arabic'])
  # response = analize('call-cut.mp3', expected_languages=['English', 'Arabic', 'Hindi','Urdu'])
  
  # specify file, possible languages and client_id
  response = analize(
      'call-cut.mp3',
      client_id='addjo30-2er3fvd', 
      expected_languages=['English', 'Arabic', 'Hindi','Urdu'])
  
  # check if request failed
  if response.status_code != 200:
      print(response.text)
      raise Exception("API responded with status code: {}".format(response.status_code))
  # get results as a dict
  response_dict = response.json()
  # show the results
  print('results:')
  print(json.dumps(response_dict, indent=2, ensure_ascii=False))
