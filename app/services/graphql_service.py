import os

import graphene
from sqlmodel import Session, create_engine, select
from starlette_graphene3 import GraphQLApp
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from models.exercises import MuscleGroupModel, Exercise, Training, ExerciseMuscleGroupLink

# Replace with your database URL
DATABASE_URL = f"postgresql+asyncpg://{os.environ.get("DB_USER", 'postgres')}:{os.environ.get("DB_PASS", 'test')}@{os.environ.get("DB_DOMAIN", 'pg_training')}/postgres"

# Create async engine
engine = create_async_engine(DATABASE_URL, future=True, echo=True)

# Create a session factory for async sessions
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# GraphQL Types
class MuscleGroupModelType(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()


class ExerciseType(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()
    engagements = graphene.List(lambda: ExerciseMuscleGroupLinkType)


class ExerciseMuscleGroupLinkType(graphene.ObjectType):
    exercise_id = graphene.Int()
    muscle_group_id = graphene.Int()
    engagement = graphene.Float()
    exercise = graphene.Field(lambda: ExerciseType)
    muscle_group = graphene.Field(lambda: MuscleGroupModelType)


class ExercisePerformedType(graphene.ObjectType):
    id = graphene.String()
    sets = graphene.Int()
    exercise = graphene.Field(lambda: ExerciseType)


class TrainingType(graphene.ObjectType):
    id = graphene.String()
    exercisesperformed = graphene.List(lambda: TrainingExercisePerformedLinkType)


class TrainingExercisePerformedLinkType(graphene.ObjectType):
    training_id = graphene.String()
    exerciseperformed_id = graphene.String()
    exerciseperformed = graphene.Field(lambda: ExercisePerformedType)
    training = graphene.Field(lambda: TrainingType)


DATABASE_URL = f"postgresql://{os.environ.get("DB_USER", 'postgres')}:{os.environ.get("DB_PASS", 'test')}@{os.environ.get("DB_DOMAIN", 'pg_training')}/postgres"
engine = create_engine(DATABASE_URL, echo=True)

# GraphQL Queries
class Query(graphene.ObjectType):
    musclegroups = graphene.List(MuscleGroupModelType)
    exercises = graphene.List(ExerciseType)
    trainings = graphene.List(TrainingType)

    def resolve_musclegroups(self, info):
        with Session(engine) as session:
            return session.exec(select(MuscleGroupModel)).all()

    def resolve_exercises(self, info):
        with Session(engine) as session:
            return session.exec(select(Exercise)).all()

    def resolve_trainings(self, info):
        with Session(engine) as session:
            return session.exec(select(Training)).all()


# GraphQL Mutations
class CreateExercise(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        muscle_group_ids = graphene.List(graphene.Int, required=True)
        engagements = graphene.List(graphene.Float, required=True)

    exercise = graphene.Field(ExerciseType)

    async def mutate(self, info, name, muscle_group_ids, engagements):
        async with async_session() as session:
            async with session.begin():
                # Create the exercise instance
                exercise = Exercise(name=name)
                session.add(exercise)
                await session.flush()  # Ensures the ID is assigned

                # Add muscle group links
                if muscle_group_ids:
                    for muscle_group_id, engagement in zip(muscle_group_ids, engagements):
                        muscle_group = await session.get(MuscleGroupModel, muscle_group_id)
                        if muscle_group:
                            link = ExerciseMuscleGroupLink(
                                exercise_id=exercise.id,
                                muscle_group_id=muscle_group.id,
                                engagement=engagement
                            )
                            session.add(link)

            # Commit the transaction to persist all changes
            await session.commit()

        return CreateExercise(exercise=exercise)


class Mutation(graphene.ObjectType):
    create_exercise = CreateExercise.Field()


# Define the context function for database session
async def context_value(request):
    async with async_session() as session:
        return {"session": session}


schema = graphene.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLApp(schema=schema, context_value=context_value)

