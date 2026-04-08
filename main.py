import json
import os

class Quiz:
    """개별 퀴즈 정보"""
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = int(answer)

    def to_dict(self):
        return {"question": self.question, "choices": self.choices, "answer": self.answer}

    def display_quiz(self, index):
        print(f"\nQ{index}. {self.question}")
        for i, choice in enumerate(self.choices, 1):
            print(f"  {i}) {choice}")

    def check_answer(self, user_input):
        return self.answer == user_input


class QuizGame:
    """게임 데이터와 로직 담당"""
    def __init__(self):
        self.quizzes = []
        self.best_score = 0
        self.load_data()

    def load_data(self):
        if not os.path.exists("state.json"):
            self.set_default_quizzes()
            return
        try:
            with open("state.json", 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.best_score = data.get("best_score", 0)
                self.quizzes = [Quiz(**q) for q in data.get("quizzes", [])]
        except (json.JSONDecodeError, IOError):
            self.set_default_quizzes()

    def save_data(self):
        try:
            data = {"best_score": self.best_score, "quizzes": [q.to_dict() for q in self.quizzes]}
            with open("state.json", 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except IOError as e:
            print(f"저장 실패: {e}")

    def set_default_quizzes(self):
        self.quizzes = [
            Quiz("Python의 창시자는?", ["Guido van Rossum", "Elon Musk", "Bill Gates", "Mark Zuckerberg"], 1),
            Quiz("JSON의 약자는?", ["Java Standard Object Notation", "JavaScript Object Notation", "Just Simple Object Note", "Jupyter System Object Network"], 2),
            Quiz("대한민국 수도는?", ["서울", "부산", "제주", "대구"], 1),
            Quiz("무지개에 없는 색은?", ["빨간색", "파란색", "노란색", "검정색"], 4),
            Quiz("영어 알파벳 개수는?", ["24개", "25개", "26개", "27개"], 3)
        ]
        self.save_data()

    def add_new_quiz(self, question, choices, answer):
        """퀴즈 추가"""
        self.quizzes.append(Quiz(question, choices, answer))
        self.save_data()
        
    def update_best_score(self, score):
        """점수를 비교하고 갱신하"""
        if score > self.best_score:
            self.best_score = score
            self.save_data()
            return True
        return False


class Menu:
    """사용자와 소통하는 '프론트엔드 (화면)'"""
    def __init__(self):
        # Menu가 시작될 때 QuizGame 엔진을 하나 장착합니다!
        self.engine = QuizGame() 

    def get_valid_input(self, prompt, min_val, max_val):
        while True:
            try:
                val = int(input(prompt).strip())
                if min_val <= val <= max_val: return val
                print(f"{min_val}~{max_val} 사이를 입력하세요.")
            except ValueError: print("숫자만 입력 가능합니다.")

    def run_play_quiz(self):
        """퀴즈 풀기 화면과 진행"""
        quizzes = self.engine.quizzes # 엔진에서 퀴즈 목록을 가져옴
        if not quizzes:
            print("\n[알림] 등록된 퀴즈가 없습니다.")
            return

        print(f"\n--- 퀴즈 시작! (현재 최고 점수: {self.engine.best_score}) ---")
        current_score = 0
        for i, quiz in enumerate(quizzes, 1):
            quiz.display_quiz(i)
            user_ans = self.get_valid_input("정답 입력 (1-4): ", 1, 4)
            if quiz.check_answer(user_ans):
                print("✅ 정답입니다!")
                current_score += 1
            else:
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번입니다.")

        print(f"\n[결과] {len(quizzes)}문제 중 {current_score}문제 정답!")
        
        # 엔진에게 점수 갱신을 부탁하고, 결과에 따라 축하 메시지 출력
        if self.engine.update_best_score(current_score):
            print(f"🎊 최고 점수 경신!")

    def run_add_quiz(self):
        """퀴즈 추가 화면"""
        print("\n--- 새로운 퀴즈 등록 ---")
        question = input("문제 내용: ").strip()
        choices = [input(f"선택지 {i}번: ").strip() for i in range(1, 5)]
        answer = self.get_valid_input("정답 번호 (1-4): ", 1, 4)
        
        # 입력받은 데이터를 엔진에 넘겨서 저장
        self.engine.add_new_quiz(question, choices, answer)
        print("\n✅ 퀴즈가 저장되었습니다!")

    def run(self):
        """메인 메뉴 화면"""
        while True:
            try:
                print("\n===== QUIZ GAME =====")
                print(f"1. 퀴즈 풀기 (현재 {len(self.engine.quizzes)}문제)")
                print("2. 퀴즈 추가")
                print("3. 퀴즈 목록 확인")
                print("4. 최고 점수 확인")
                print("5. 종료")
                
                choice = self.get_valid_input("메뉴 선택: ", 1, 5)

                if choice == 1: self.run_play_quiz()
                elif choice == 2: self.run_add_quiz()
                elif choice == 3:
                    print("\n--- 등록된 퀴즈 목록 ---")
                    for i, q in enumerate(self.engine.quizzes, 1):
                        print(f"{i}. {q.question}")
                elif choice == 4:
                    print(f"\n시스템 최고 점수: {self.engine.best_score}점")
                elif choice == 5:
                    print("프로그램을 종료합니다.")
                    self.engine.save_data()
                    break
            except (KeyboardInterrupt, EOFError):
                self.engine.save_data()
                break

if __name__ == "__main__":
    app = Menu() 
    app.run()