import dialogflow_v2

def create_intent(project_id, display_name, training_phrases_parts,
                  message_texts):
    """Create an intent of the given intent type."""
    intents_client = dialogflow_v2.IntentsClient()

    parent = intents_client.project_agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow_v2.types.Intent.TrainingPhrase.Part(
            text=training_phrases_part)
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow_v2.types.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow_v2.types.Intent.Message.Text(text=message_texts)
    message = dialogflow_v2.types.Intent.Message(text=text)

    intent = dialogflow_v2.types.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message])
    try :
        response = intents_client.create_intent(parent, intent)
        print('Intent created: {}'.format(response))
    except Exception as e :
        print "google.api_core.exceptions.FailedPrecondition: "+str(e)
    

def list_intents(project_id):
    intents_client = dialogflow_v2.IntentsClient()

    parent = intents_client.project_agent_path(project_id)

    intents = intents_client.list_intents(parent)

    for intent in intents:
        print('=' * 20)
        # print('Intent name: {}'.format(intent.name))
        print('Intent display_name: {}'.format(intent.display_name))
        # print('Action: {}\n'.format(intent.action))
        # print('Root followup intent: {}'.format(
        #     intent.root_followup_intent_name))
        # print('Parent followup intent: {}\n'.format(
        #     intent.parent_followup_intent_name))

        # print('Input contexts:')
        # for input_context_name in intent.input_context_names:
        #     print('\tName: {}'.format(input_context_name))

        # print('Output contexts:')
        # for output_context in intent.output_contexts:
        #     print('\tName: {}'.format(output_context.name))

def _get_intent_ids(project_id, display_name): # leading underscore implies the weak "internal use" indicator...
    intents_client = dialogflow_v2.IntentsClient()

    parent = intents_client.project_agent_path(project_id)
    intents = intents_client.list_intents(parent)
    intent_names = [
        intent.name for intent in intents
        if intent.display_name == display_name]

    intent_ids = [
        intent_name.split('/')[-1] for intent_name
        in intent_names]

    return intent_ids

def delete_intent(project_id, display_name):
    """Delete intent with the given intent type and intent value."""
    intents_client = dialogflow_v2.IntentsClient()

    intent_path = intents_client.intent_path(project_id, _get_intent_ids(project_id,display_name)[0])

    intents_client.delete_intent(intent_path)

if __name__=='__main__':
    project_id = 'test1-98fad'
    create_intent(project_id,'v2test',['train1','train2'],['resp1','resp2'])
    list_intents(project_id)
    #delete_intent(project_id,'v2test')
    #list_intents(project_id)