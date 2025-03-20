from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Question, Interview,interviewVideo,InterviewEvaluation

User=get_user_model()

# Here we defined the serializer class for our User model
# Serializers act as a bridge between django model objects and JSON data when we are using RESTAPI framework
class UserSignUpSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True,required=True)
    password2=serializers.CharField(write_only=True,required=True)

    class Meta:
        model=User
        fields=(
            'username',
            'email',
            'password',
            'password2'
        )
    def validate(self,data):
            if data.get('password') != data.get('password2'):
                raise serializers.ValidationError("Password does not match")
            return data
    def create(self,validated_data):
            password = validated_data.pop('password')
            validated_data.pop('password2',None)
            user=User(**validated_data)
            user.set_password(password)
            user.save()
            return user
    
# Here we defined the serializer class for our Question model
class QuestionSerializer(serializers.ModelSerializer):
      class Meta:
            model = Question
            fields = ['id','question_text']

# Here we defined the serializer class for our Interview model
class InterviewSerializer(serializers.ModelSerializer):
      questions = QuestionSerializer(many=True,write_only = True)

      class Meta:
            model = Interview
            fields = ['id','title','description','questions']

      def create(self, validated_data):
            questions_data = validated_data.pop('questions')
            interview = Interview.objects.create(**validated_data)
            Question.objects.bulk_create([Question(interview=interview, **q) for q in questions_data])
            return interview

class InterviewVideoSerializer(serializers.ModelSerializer):
      
      class Meta:
            model = interviewVideo
            fields =['id','video_title','video_file','video_url','duration','uploaded_at']
            read_only_fields=['video_url','duration','uploaded_at']


class EvaluationSerializer(serializers.ModelSerializer):
      class Meta:
            model = InterviewEvaluation
            fields = ['id','evaluator','score','comments','created_at']
            read_only_fields=['id','created_at']