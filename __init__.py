from mycroft import MycroftSkill, intent_file_handler


class ModelManager(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('manager.model.intent')
    def handle_manager_model(self, message):
        self.speak_dialog('manager.model')


def create_skill():
    return ModelManager()

