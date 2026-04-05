import json
import os

class Quiz:
    """개별 퀴즈 정보를 담는 클래스"""
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = int(answer)

    def display_quiz(self, index):
        """문제와 선택지를 화면에 출력"""
        print(f"\nQ{index}. {self.question}")
        for i, choice in enumerate(self.choices, 1):
            print(f"  {i}) {choice}")

    def check_answer(self, user_input):
        """정답 여부 확인"""
        return self.answer == user_input

class Menu:
    """메뉴 및 게임 흐름 관리 클래스"""
    def __init__(self):
        self.quizzes = []
        self.best_score = 0
        self.set_default_quizzes() # 1. 시작할 때 퀴즈 목록을 채웁니다!

    def set_default_quizzes(self):
        """기본 퀴즈 5개 생성 (Menu 클래스 안으로 이동)"""
        q1 = Quiz("Python의 창시자는?", ["Guido van Rossum", "Elon Musk", "Bill Gates", "Mark Zuckerberg"], 1)
        q2 = Quiz("리스트에 요소를 추가하는 메서드는?", ["add()", "push()", "append()", "insert_end()"], 3)
        q3 = Quiz("불리언(Boolean) 타입이 아닌 것은?", ["True", "False", "None", "1 == 1"], 3)
        q4 = Quiz("JSON의 약자는?", ["Java Standard Object Notation", "JavaScript Object Notation", "Just Simple Object Note", "Jupyter System Object Network"], 2)
        q5 = Quiz("Python에서 주석을 쓸 때 사용하는 기호는?", ["//", "/* */", "", "#"], 4)
        
        self.quizzes = [q1, q2, q3, q4, q5]

    def get_valid_input(self, prompt, min_val, max_val): 
        """예외처리 메소드"""
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
        """퀴즈 풀기 로직"""
        if not self.quizzes:
            print("\n[알림] 현재 등록된 퀴즈가 없습니다.")
            return

        print(f"\n--- 퀴즈를 시작합니다! (총 {len(self.quizzes)}문제) ---")
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
        
        if current_score > self.best_score:
            print(f"🎊 최고 기록 달성! ({self.best_score} -> {current_score})")
            self.best_score = current_score

    def run(self):
        """메인 메뉴 루프"""
        while True:
            try:
                print("\n===== QUIZ GAME =====")
                print("1. 퀴즈 풀기")
                print("2. 퀴즈 추가 (준비중)")
                print("3. 퀴즈 목록 (준비중)")
                print("4. 최고 점수 확인")
                print("5. 종료")
                
                choice = self.get_valid_input("메뉴 선택: ", 1, 5)

                if choice == 1: 
                    self.play_quiz() # 2. 준비 중 메시지 대신 진짜 기능 연결!
                elif choice == 4:
                    print(f"\n현재 최고 점수: {self.best_score}점")
                elif choice == 5:
                    print("프로그램을 종료합니다.")
                    break
                else:
                    print("-> 아직 준비 중인 기능입니다.")
                    
            except (KeyboardInterrupt, EOFError):
                print("\n\n프로그램을 안전하게 종료합니다.")
                break

if __name__ == "__main__":
    game = Menu()
    game.run()