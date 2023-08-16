import random
import time

class Question:
    def __init__(self, question, answer, choices=None, difficulty=1, category='General'):
        self.question = question
        self.answer = answer
        self.choices = choices
        self.difficulty = difficulty
        self.category = category

    def is_multiple_choice(self):
        return self.choices is not None

    def is_correct(self, user_answer):
        return user_answer.lower() == self.answer.lower()

class QuizMaker:
    def __init__(self, questions_file):
        self.questions_file = questions_file
        self.questions = self.read_questions()

    def read_questions(self):
        questions = []
        with open(self.questions_file, 'r') as file:
            for line in file:
                data = line.strip().split('|')
                question = data[0]
                answer = data[1]
                choices = data[2].split(',') if len(data) > 2 else None
                difficulty = int(data[3]) if len(data) > 3 else 1
                category = data[4] if len(data) > 4 else 'General'
                questions.append(Question(question, answer, choices, difficulty, category))
        return questions

    def select_quiz_questions(self, num_questions, categories=None, difficulty=None):
        if categories:
            selected_questions = [q for q in self.questions if q.category in categories]
        else:
            selected_questions = self.questions

        if difficulty:
            selected_questions = [q for q in selected_questions if q.difficulty == difficulty]

        random.shuffle(selected_questions)
        return selected_questions[:num_questions]

    def take_quiz(self, num_questions=10, categories=None, difficulty=None):
        quiz_questions = self.select_quiz_questions(num_questions, categories, difficulty)
        score = 0
        start_time = time.time()

        for i, question in enumerate(quiz_questions, start=1):
            print(f'\nQuestion {i}/{num_questions} - [{question.category}] (Difficulty: {question.difficulty})')
            print(question.question)

            if question.is_multiple_choice():
                for idx, choice in enumerate(question.choices, start=1):
                    print(f'{idx}. {choice}')

            user_answer = input('Your answer: ').strip()

            if question.is_correct(user_answer):
                print('Correct!\n')
                score += 1
            else:
                print(f'Incorrect. The correct answer is: {question.answer}\n')

        end_time = time.time()
        elapsed_time = end_time - start_time
        return score, elapsed_time

if __name__ == '__main__':
    questions_file = 'quiz_questions.txt'
    quiz_maker = QuizMaker(questions_file)

    print('Welcome to the Quiz Maker!')
    num_questions = int(input('Enter the number of questions you want in the quiz: '))
    categories = input('Enter the categories you want to include (comma-separated, or leave empty for all): ').split(',')
    difficulty = int(input('Enter the difficulty level you want (1, 2, or 3): '))

    score, elapsed_time = quiz_maker.take_quiz(num_questions, categories, difficulty)
    print(f'\nQuiz completed!\nYour score: {score}/{num_questions}\nTotal time taken: {elapsed_time:.2f} seconds')