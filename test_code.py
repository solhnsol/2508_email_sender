import time
from send_email import notify_on_finish

# 데코레이터 적용 예시
@notify_on_finish(to_email="jayhanss@gmail.com")
def train_my_model(epochs):
    print(f"모델 학습 시작 (총 {epochs} 에포크)")
    for i in range(epochs):
        time.sleep(1)
        print(f"에포크 {i+1}/{epochs} 완료")
    print("모델 학습 종료!")
    return "학습 완료 메시지"

if __name__ == "__main__":
    # 성공적으로 실행될 함수
    train_my_model(3)