from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_file_handler, intent_handler
import networkx as nx
import nltk
from mycroft.util import LOG
from .lib.CyberHouseClient import CyberHouseClient

class ModelManager(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.client = CyberHouseClient(LOG, "GPT2Client")
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')
        nltk.download('universal_tagset')
        self.contextSet = []
        self.G = nx.DiGraph()
        # somecomment

    @intent_file_handler('manager.model.intent')
    def handle_manager_model(self, message):
        # acquire object name from user
        vertice_name = self.get_response('object.name')
        self.G.add_node(vertice_name)
        vertices = list(self.G.nodes)
        vertice_list = ', '.join(str(v) for v in vertices)
        self.speak('{}'.format(vertice_list))
        # acquire relationship to another object
        #self.speak_dialog('manager.model')

    @intent_handler(IntentBuilder('ConnectContext').require('Connect').require('Source').require('To').require('Target'))
    def handle_connect(self, message):
        source = message.data.get('Source')
        target = message.data.get('Target')
        self.speak('How does {} relate to {}'.format(source, target))

    @intent_handler(IntentBuilder('DescribeContext').require('Define').require('Relation'))
    def handle_define_relation(self, message):
        sentence = self.get_response('provide.object.relation.object') + "."
        self.speak('Did, I get it right? {}'.format(sentence))
        tokens = nltk.word_tokenize(sentence)
        tagged_tokens = nltk.pos_tag(tokens)
        tagged_tokens_str = ', '.join(str(word) + "(" + str(tag) + ")" for word,tag in tagged_tokens)
        self.log.info("name={0}".format(tagged_tokens_str))

    @intent_handler(IntentBuilder('CapabilityContext').require('Define').require('Capability'))
    def handle_define_capability(self, message):
        # What is being provided
        goal = self.get_response('provide.goal')
        # When
        context = self.get_response('provide.context')
        # How
        ability = self.get_response('provide.ability')
        # What is required
        capacity = self.get_response('provide.capacity')

        self.speak('Would you like to {} {}?'.format(goal, context))
        self.speak('Can you {}?'.format(ability))
        self.speak('Do you have {}?'.format(capacity))

        # GPT-2 Response
        response = self.client.request("I want to {} {}. I need {} and I have to {} to".format(goal, context, capacity, ability))
        self.speak('{}'.format(response))
        #tokens = nltk.word_tokenize(sentence)
        #tagged_tokens = nltk.pos_tag(tokens)
        #tagged_tokens_str = ', '.join(str(word) + "(" + str(tag) + ")" for word,tag in tagged_tokens)
        breakdown = "Capacity: Goal:{0}, Context: {1}, Ability: {2}, Capacity: {3}".format(goal, context, ability, capacity)
        self.speak('{}'.format(breakdown))
        self.log.info('{}'.format(breakdown))

    #def ask_object(self, a, b):
    #    sentence = self.get_response('provide.object.relation.object') + "."

def create_skill():
    return ModelManager()
