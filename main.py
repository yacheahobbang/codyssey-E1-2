import json
import os

class Quiz:
    """
    개별 퀴즈 한 개의 정보를 관리하는 클래스
    """
    def __init__(self, question, choices, answer):
        """
        퀴즈 인스턴스 생성 시 실행되는 초기화 메소드
        :param question: 문제 내용 (문자열)
        :param choices: 4개의 선택지 (리스트)
        :param answer: 정답 번호 1~4 (정수)
        """
        self.question = question
        self.choices = choices
        self.answer = int(answer)

    def to_dict(self):
        """
        객체 데이터를 JSON 파일로 저장하기 위해 딕셔너리 형태로 변환하는 메소드
        """
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer
        }

    def display_quiz(self, index):
        """
        화면에 문제와 번호가 매겨진 선택지들을 출력하는 메소드
        """
        print(f"\nQ{index}. {self.question}")
        for i, choice in enumerate(self.choices, 1):
            print(f"  {i}) {choice}")

    def check_answer(self, user_input):
        """
        사용자가 입력한 번호와 실제 정답 번호가 일치하는지 확인하는 메소드
        """
        return self.answer == user_input


class Menu:
    """
    게임의 전체적인 흐름, 메뉴 관리, 데이터 저장/불러오기를 담당하는 클래스
    """
    def __init__(self):
        """
        게임 시작 시 변수를 준비하고 데이터를 불러오는 초기화 메소드
        """
        self.quizzes = [] # 퀴즈 객체들을 담을 바구니
        self.best_score = 0 # 최고 점수 기록
        self.load_data() # 프로그램 시작 시 파일에서 데이터 읽어오기

    def load_data(self):
        """
        state.json 파일에서 데이터를 불러오는 메소드. 
        파일이 없거나 손상되었다면 기본 퀴즈 5개를 세팅함.
        """
        if not os.path.exists("state.json"):
            self.set_default_quizzes()
            return
        try:
            with open("state.json", 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.best_score = data.get("best_score", 0)
                # JSON의 딕셔너리 데이터를 다시 Quiz 클래스의 인스턴스로 복구
                self.quizzes = [Quiz(**q) for q in data.get("quizzes", [])]
        except (json.JSONDecodeError, IOError):
            print("\n[알림] 데이터 파일이 손상되었습니다. 기본 데이터로 복구합니다.")
            self.set_default_quizzes()

    def save_data(self):
        """
        현재 퀴즈 목록과 최고 점수를 state.json 파일에 물리적으로 저장하는 메소드
        """
        try:
            data = {
                "best_score": self.best_score,
                "quizzes": [q.to_dict() for q in self.quizzes]
            }
            with open("state.json", 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except IOError as e:
            print(f"\n[오류] 파일 저장 중 문제가 발생했습니다: {e}")

    def set_default_quizzes(self):
        """
        최초 실행 시 사용할 5개의 기본 퀴즈 데이터를 생성하는 메소드
        """
        q1 = Quiz("Python의 창시자는?", ["Guido van Rossum", "Elon Musk", "Bill Gates", "Mark Zuckerberg"], 1)
        q2 = Quiz("리스트에 요소를 추가하는 메서드는?", ["add()", "push()", "append()", "insert_end()"], 3)
        q3 = Quiz("불리언(Boolean) 타입이 아닌 것은?", ["True", "False", "None", "1 == 1"], 3)
        q4 = Quiz("JSON의 약자는?", ["Java Standard Object Notation", "JavaScript Object Notation", "Just Simple Object Note", "Jupyter System Object Network"], 2)
        q5 = Quiz("Python에서 주석을 쓸 때 사용하는 기호는?", ["//", "/* */", "", "#"], 4)
        
        self.quizzes = [q1, q2, q3, q4, q5]
        self.save_data() # 생성 후 바로 저장

    def get_valid_input(self, prompt, min_val, max_val):
        """
        숫자 입력 시 예외 처리를 담당하는 메소드.
        범위를 벗어나거나 문자를 입력하면 다시 입력을 받음.
        """
        while True:
            try:
                user_input = input(prompt).strip()
                if not user_input:
                    print("입력이 비어 있습니다. 다시 입력해 주세요.")
                    continue
                value = int(user_input)
                if min_val <= value <= max_val:
                    return value
                else:
                    print(f"{min_val}~{max_val} 사이의 숫자를 입력해 주세요.")
            except ValueError:
                print("숫자만 입력 가능합니다. 다시 시도하세요.")

    def play_quiz(self):
        """
        1번 메뉴: 저장된 퀴즈를 순서대로 풀고 점수를 계산하는 메소드
        """
        if not self.quizzes:
            print("\n[알림] 등록된 퀴즈가 없습니다.")
            return

        print(f"\n--- 퀴즈를 시작합니다! (현재 최고 점수: {self.best_score}) ---")
        current_score = 0

        for i, quiz in enumerate(self.quizzes, 1):
            quiz.display_quiz(i)
            user_ans = self.get_valid_input("정답 입력 (1-4): ", 1, 4)
            
            if quiz.check_answer(user_ans):
                print("✅ 정답입니다!")
                current_score += 1
            else:
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번입니다.")

        print(f"\n[최종 결과] {len(self.quizzes)}문제 중 {current_score}문제를 맞혔습니다!")
        
        # 최고 점수 경신 시 데이터 업데이트 및 저장
        if current_score > self.best_score:
            print(f"🎊 축하합니다! 최고 기록 달성: {current_score}점")
            self.best_score = current_score
            self.save_data()

    def add_quiz(self):
        """
        2번 메뉴: 사용자로부터 새로운 문제를 입력받아 추가하는 메소드
        """
        print("\n--- 새로운 퀴즈 등록 ---")
        while True:
            question = input("문제 내용을 입력하세요: ").strip()
            if question: break
            print("문제 내용은 필수입니다.")

        choices = []
        for i in range(1, 5):
            while True:
                choice = input(f"선택지 {i}번 내용을 입력하세요: ").strip()
                if choice:
                    choices.append(choice)
                    break
                print("선택지 내용은 필수입니다.")

        answer = self.get_valid_input("정답 번호를 입력하세요 (1-4): ", 1, 4)
        
        self.quizzes.append(Quiz(question, choices, answer))
        self.save_data() # 추가 즉시 파일에 저장
        print("\n✅ 퀴즈가 성공적으로 추가되었습니다!")

    def run(self):
        """
        메인 메뉴 루프를 실행하여 사용자의 선택을 기다리는 메소드
        """
        while True:
            try:
                print("\n===== QUIZ GAME =====")
                print(f"1. 퀴즈 풀기 (현재 {len(self.quizzes)}문제)")
                print("2. 퀴즈 추가")
                print("3. 퀴즈 목록 확인")
                print("4. 최고 점수 확인")
                print("5. 종료")
                
                choice = self.get_valid_input("메뉴 선택: ", 1, 5)

                if choice == 1: self.play_quiz()
                elif choice == 2: self.add_quiz()
                elif choice == 3:
                    print("\n--- 현재 등록된 퀴즈 목록 ---")
                    for i, q in enumerate(self.quizzes, 1):
                        print(f"{i}. {q.question}")
                elif choice == 4:
                    print(f"\n현재 시스템 최고 점수: {self.best_score}점")
                elif choice == 5:
                    print("프로그램을 종료합니다.")
                    self.save_data() # 종료 전 최종 저장
                    break
                    
            except (KeyboardInterrupt, EOFError):
                print("\n\n프로그램을 안전하게 종료합니다.")
                self.save_data()
                break

# 프로그램 실행의 메인 스위치
if __name__ == "__main__":
    game = Menu()
    game.run()