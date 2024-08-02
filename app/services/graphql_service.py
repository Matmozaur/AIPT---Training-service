import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from sqlmodel import Session, select
from models import (
    MuscleGroupModel,
    Exercise,
    ExerciseMuscleGroupLink,
    ExercisePerformed,
    Training,
    TrainingExercisePerformedLink,
)
from database import engine

# GraphQL Types
class MuscleGroupModelType(SQLAlchemyObjectType):
    class Meta:
        model = MuscleGroupModel

class ExerciseType(SQLAlchemyObjectType):
    class Meta:
        model = Exercise

class ExerciseMuscleGroupLinkType(SQLAlchemyObjectType):
    class Meta:
        model = ExerciseMuscleGroupLink

class ExercisePerformedType(SQLAlchemyObjectType):
    class Meta:
        model = ExercisePerformed

class TrainingType(SQLAlchemyObjectType):
    class Meta:
        model = Training

class TrainingExercisePerformedLinkType(SQLAlchemyObjectType):
    class Meta:
        model = TrainingExercisePerformedLink

# GraphQL Query
class Query(graphene.ObjectType):
    musclegroups = graphene.List(MuscleGroupModelType)
    exercises = graphene.List(ExerciseType)
    trainings = graphene.List(TrainingType)

    def resolve_musclegroups(self, info):
        query = select(MuscleGroupModel)
        with Session(engine) as session:
            return session.exec(query).all()

    def resolve_exercises(self, info):
        query = select(Exercise)
        with Session(engine) as session:
            return session.exec(query).all()

    def resolve_trainings(self, info):
        query = select(Training)
        with Session(engine) as session:
            return session.exec(query).all()

# GraphQL Mutation
class CreateExercise(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        muscle_group_ids = graphene.List(graphene.Int, required=False)
        engagement = graphene.Float(required=False)

    exercise = graphene.Field(lambda: ExerciseType)

    def mutate(self, info, name, muscle_group_ids=None, engagement=0):
        with Session(engine) as session:
            exercise = Exercise(name=name)
            session.add(exercise)
            session.commit()
            session.refresh(exercise)

            if muscle_group_ids:
                for muscle_group_id in muscle_group_ids:
                    muscle_group = session.get(MuscleGroupModel, muscle_group_id)
                    if muscle_group:
                        link = ExerciseMuscleGroupLink(
                            exercise_id=exercise.id,
                            muscle_group_id=muscle_group.id,
                            engagement=engagement
                        )
                        session.add(link)

                session.commit()

        return CreateExercise(exercise=exercise)

class Mutation(graphene.ObjectType):
    create_exercise = CreateExercise.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
