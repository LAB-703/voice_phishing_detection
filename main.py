import streamlit as st
import os
import openai

type_options = ["fraud", "imperson"]
num_options = [1, 2, 3, 4, 5]

manual = '''
1. 기존 수법 예방수칙
1) 기관사칭
수사기관·금융기관이라며 자금 이체나 금융정보 요구하면, 100% 보이스피싱 
검찰·경찰·금감원 등 정부기관은 절대 전화로 자금 이체 또는 금융정보를 요구하지 않음
범인은 공무원증‧영장 등을 사진으로 보내며, “계좌에 잔액이 총 얼마냐”, “계좌가 자금세탁 등 범죄에 이용되었다”, “현금을 인출해서 냉장고에 보관해라” 등 치밀하게 접근
통화내용을 절대 타인에게 발설하지 말라고 하면, 100% 보이스피싱 
범인은 “극비수사 중이니, 절대 타인에게 발설하지 말라”, “조용한 곳에서 전화를 받아라”, “비협조 시 구속수사 하겠다“고 말하는 등 협박을 통해 피해자를 심리적으로 압박

2) 대출사기
전화·문자로 대출을 권유하고 처리비용을 요구하면, 100% 보이스피싱 
대출을 권유하는 자가 금융회사 정식 직원인지 확인 후에 대응
※ 금융회사 조회(금감원) : www.fss.or.kr / 대출모집인 조회 : www.loanconsultant.or.kr

3) 정보탈취
금융기관 팝업창에 금융거래정보 입력 요구하면, 100% 보이스피싱 
인터넷 포털사이트 접속시, 보안 관련 인증 절차를 강화한다는 이유로 금감원이나 금융기관 팝업창을 띄워 계좌번호·비밀번호·보안카드 번호를 요구하면 100% 사기

4) 스미싱 파밍
출처 불명 파일·이메일·문자는 절대 클릭하지 말고 즉시 삭제·차단 
택배 배송조회·건강검진 결과조회·무료쿠폰 제공 등 링크(URL) 클릭 시, 휴대전화에 악성코드가 설치되고 범인은 원격으로 휴대전화를 조종하여 자금 이체 및 개인정보 탈취
※ 악성코드 치료방법 : 한국인터넷진흥원 홈페이지 ‘보호나라’ → 공지사항(108번) 참고

5) 납치사기
자녀납치 협박전화를 받은 경우, 일단 전화를 끊고 자녀 안전 확인 
딥페이크(합성) 등 AI기술을 이용해 실제 자녀 사진을 보여주거나 목소리를 들려주며 협박하는 경우도 있으므로, 일절 대응하지 말고, 직접 자녀에게 전화하거나 대면하여 안전 확인

6) 가족사칭
문자·메신저를 통해 가족 사칭 금전 요구하는 경우, 반드시 확인 
범인들은 카카오톡 프로필을 조작하여 가족인 척 금전을 요구하는 사례가 많으므로, 반드시 유선으로 가족이 보낸 메시지가 맞는지 확인

2. 신종 수법 예방수칙
1) 몸캠피싱
채팅앱에서 음란 영상통화 제안 시, 피싱조직이므로 절대 응하지 말 것 
만남어플 채팅을 통해 여성행세를 하며 접근하여 음란 영상통화를 제안한 후, 녹화된 음란행위 장면을 유포하겠다고 협박하여 금품을 갈취하는 수법에 20~30대 남성 피해 심각

2) 마약피싱
타인이 건네는 출처 불명의 음료·음식은 확인되기 전까지 섭취 금지 
최근, 학생들을 대상으로 집중력 향상에 도움이 된다고 속여 마약 음료를 마시게 한 후, 이를 빌미로 학부모들을 협박하여 금전을 갈취하는 신종 수법 발생

3) 통장협박
모르는 돈이 입금되면 즉시 금융기관에 신고하여 환급 절차 진행 
계좌가 공개된 자영업자 등에게 돈을 송금 후, 보이스피싱 계좌라고 허위 신고하여 피해자 계좌를 지급정지 시켜 이를 해제하는 대가로 금전을 갈취하는 통장협박 수법 유행

3. 피해구제 신청
피해구제
보이스피싱 피해 발생시, 즉시 신고 후 피해금 환급 신청 
사기범에게 돈을 이체한 경우, 신속히 경찰이나 금융회사에 전화하여 지급정지 등 조치
※ 조치순서 : 지급정지 신청(금융회사) → 피해신고(112) → 피해금 환급신청(금융회사)
'''

st.title("Voice Phishing Detection and Prevention")

st.write("Enter your OpenAI API key:")
api_key = st.text_input(placeholder = "sk-XXXXXXXXXXX", type="password")

st.write("Choose the type and number of the audio sample to analyze.")

type_choice = st.selectbox("Select type", type_options)
num_choice = st.selectbox("Select number", num_options)

if api_key:
    openai.api_key = api_key
    
    if st.button("Analyze"):
        with st.spinner("Transcribing and analyzing the audio..."):
            voice_file_path = f"audio_data/{type_choice}_{num_choice}.mp3"
            if os.path.exists(voice_file_path):
                voice_file = open(voice_file_path, "rb")
                transcription = openai.Audio.transcribe("whisper-1", voice_file)

                prompt = f"""
                아래 보이스피싱 관련 [매뉴얼]을 보고, [통화 내용]에 대한 보이스 피싱 유형을 분류하시오.
                그에 적절한 대처 방안을 단계별로 알려주시오.

                [매뉴얼]
                {manual}

                [통화 내용]
                {transcription['text']}
                """

                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )

                st.subheader("Transcription")
                st.write(transcription['text'])

                st.subheader("Response")
                st.write(response["choices"][0]["message"]["content"])
            else:
                st.error("Audio file not found. Please check the file path.")
else:
    st.warning("Please enter your OpenAI API key to proceed.")
