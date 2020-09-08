import json
from datetime import datetime

from django.views.generic import View
from django.http import JsonResponse
# chatterbot
from chatterbot import ChatBot, filters, corpus
from chatterbot.trainers import ChatterBotCorpusTrainer

from chatterbot.ext.django_chatterbot import settings


class ChatterBotApiView(View):
    """
    API endpoint to interact with ChatterBot.

    """

    now = datetime.now()

    # Inisialisasi Objek Chatbot
    chatterbot = ChatBot(
        name='Chatbot API',
        logic_adapters=[
            {
                'import_path': 'chatterbot.logic.BestMatch',
                'default_response': 'Maaf, aku gak ngerti'
                # jika chatbot tidak mengerti pertanyaan yang diberikan, return response ini
            },
            {
                'import_path': 'chatterbot.logic.MathematicalEvaluation'
            },
            {
                'import_path': 'chatterbot.logic.SpecificResponseAdapter',
                'input_text': 'Sekarang jam berapa?',
                'output_text': 'Sekarang jam {}:{}'.format(now.hour, now.minute)
            }
        ],
        filters=[filters.get_recent_repeated_responses],
    )

    # memasukkan data yang akan menjadi bahan pembelajaran model chatbot
    trainer = ChatterBotCorpusTrainer(chatterbot)

    trainer.train(
        # "chatterbot.corpus.indonesia",          # data training dari package
        "./api/custom.yml"  # data training dari lokal
    )

    # method untuk mendapatkan response dari chatbot
    def post(self, request, *args, **kwargs):
        """
        Return a response to the statement in the posted data.
        * The JSON data should contain a 'text' attribute.
        """
        input_data = json.loads(request.body.decode('utf-8'))

        if 'text' not in input_data:
            return JsonResponse({
                'text': [
                    'The attribute "text" is required.'
                ]
            }, status=400)

        response = self.chatterbot.get_response(input_data)

        response_data = response.serialize()

        return JsonResponse({
            'response': response_data['text'],
            'time': response_data['created_at']
        },
            status=200)

        # return JsonResponse(response_data, status=200)

    def get(self, request, *args, **kwargs):
        """
        Return data corresponding to the current conversation.
        """
        return JsonResponse({
            'name': self.chatterbot.name
        })
