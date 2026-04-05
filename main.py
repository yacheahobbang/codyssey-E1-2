import json
import os
class Quiz:
    """개별 퀴즈 정보를 담는 클래스"""
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = int(answer)

    def to_dict(self):
        """JSON 저장을 위해 딕셔너리로 변환"""
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer
        }

    def display_quiz(self, index):
        """문제와 선택지를 화면에 출력"""
        print(f"\nQ{index}. {self.question}")
        for i, choice in enumerate(self.choices, 1):
            print(f"  {i}) {choice}")

    def check_answer(self, user_input):
        """정답 여부 확인"""
        return self.answer == user_input

def set_default_quizzes(self):
        """최초 실행 시 사용할 5개의 기본 퀴즈 (주제: 파이썬 상식)"""
        
        # 요구사항: 각 퀴즈는 문제, 선택지(4개), 정답을 포함하며 Quiz 클래스의 인스턴스로 생성한다.
        q1 = Quiz("Python의 창시자는?", ["Guido van Rossum", "Elon Musk", "Bill Gates", "Mark Zuckerberg"], 1)
        q2 = Quiz("리스트에 요소를 추가하는 메서드는?", ["add()", "push()", "append()", "insert_end()"], 3)
        q3 = Quiz("불리언(Boolean) 타입이 아닌 것은?", ["True", "False", "None", "1 == 1"], 3)
        q4 = Quiz("JSON의 약자는?", ["Java Standard Object Notation", "JavaScript Object Notation", "Just Simple Object Note", "Jupyter System Object Network"], 2)
        q5 = Quiz("Python에서 주석을 쓸 때 사용하는 기호는?", ["//", "/* */", "", "#"], 4)
        
        # 요구사항: 5개 이상의 퀴즈를 직접 작성한다.
        self.quizzes = [q1, q2, q3, q4, q5]
        self.save_data() # 세팅 후 파일에 저장

class Menu:
    """메뉴 관리 클래스"""
    def __init__(self):
        # 퀴즈 목록과 최고 점수를 저장할 준비
        self.quizzes = []
        self.best_score = 0

    def get_valid_input(self, prompt, min_val, max_val): 
        """예외처리 메소드"""
        while True:
            try:
                user_input = input(prompt).strip() # 앞뒤 공백 제거
                
                if not user_input: # 빈 입력(Enter만 친 경우) 처리
                    print("입력이 비어 있습니다. 다시 입력해 주세요.")
                    continue
                
                value = int(user_input) # 숫자로 변환 시도
                
                if min_val <= value <= max_val: # 허용 범위 확인
                    return value
                else:
                    print(f"{min_val}~{max_val} 사이의 숫자를 입력해 주세요.")
                    
            except ValueError: # 문자를 입력한 경우 (숫자 변환 실패)
                print("숫자만 입력 가능합니다. 다시 시도하세요.")

    def run(self):
        """메인 메뉴 루프"""
        while True:
            try:
                print("\n===== QUIZ GAME =====")
                print("1. 퀴즈 풀기")
                print("2. 퀴즈 추가")
                print("3. 퀴즈 목록")
                print("4. 최고 점수 확인")
                print("5. 종료")
                
                # 1~5 사이의 숫자만 입력받도록 함수 호출
                choice = self.get_valid_input("메뉴 선택: ", 1, 5)

                # 선택 결과에 따른 동작 (아직 기능이 없으므로 안내문만 출력)
                if choice == 1: 
                    print("-> '퀴즈 풀기' 기능은 준비 중입니다.")
                elif choice == 2: 
                    print("-> '퀴즈 추가' 기능은 준비 중입니다.")
                elif choice == 3: 
                    print("-> '퀴즈 목록' 기능은 준비 중입니다.")
                elif choice == 4: 
                    print("-> '최고 점수 확인' 기능은 준비 중입니다.")
                elif choice == 5:
                    print("프로그램을 종료합니다.")
                    break # while 반복문을 빠져나가며 프로그램 종료
                    
            # Ctrl+C (KeyboardInterrupt) 등으로 강제 종료 시 에러 튕김 방지
            except (KeyboardInterrupt, EOFError):
                print("\n\n프로그램을 안전하게 종료합니다.")
                break

# 파이썬 파일을 실행할 때 가장 먼저 시작되는 부분
if __name__ == "__main__":
    game = QuizGame()
    game.run()