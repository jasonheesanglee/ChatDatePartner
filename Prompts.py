from han_util_unicode import join_jamos, split_syllables

class Prompts:
    def __init__(self, user_name, partner_name,
                 u_gender, p_gender, friend_type,
                 age, domain, session_id,
                 gaebang, seongsil, woehyang, chinhwa, singyung,
                 ):

        self.user_name = user_name
        self.partner_name = partner_name
        self.u_gender = u_gender
        self.p_gender = p_gender
        self.friend_type = friend_type

        self.age = age
        self.domain = domain
        self.gaebang = gaebang
        self.seongsil = seongsil
        self.woehyang = woehyang
        self.chinhwa = chinhwa
        self.singyung = singyung
        self.session_id = session_id


        if split_syllables(partner_name)[-1] in ['ㅏ', 'ㅑ', 'ㅓ', 'ㅕ',
                                                 'ㅗ', 'ㅛ', 'ㅜ', 'ㅠ',
                                                 'ㅡ', 'ㅣ', 'ㅙ', 'ㅞ',
                                                 'ㅚ', 'ㅟ', 'ㅢ', 'ㅒ',
                                                 'ㅖ']:
            self.p_syl = ['가', '야', '는', '를', '야', '', '와']  # 홍주는
        else:
            self.p_syl = ['이', '아', '이는', '을', '이야', '이', '과']  # 희상이는
        if split_syllables(user_name)[-1] in ['ㅏ', 'ㅑ', 'ㅓ', 'ㅕ',
                                              'ㅗ', 'ㅛ', 'ㅜ', 'ㅠ',
                                              'ㅡ', 'ㅣ', 'ㅙ', 'ㅞ',
                                              'ㅚ', 'ㅟ', 'ㅢ', 'ㅒ',
                                              'ㅖ']:
            self.u_syl = ['가', '야', '는', '를', '야', '', '와']  # 홍주는
        else:
            self.u_syl = ['이', '아', '이는', '을', '이야', '이', '과']  # 희상이는


    def gender_translator(self, gender):
        if '여자' in gender:
            return 'female'
        elif '남자' in gender:
            return 'male'

    def get_traits(self):
        trait = f'''
                {self.partner_name}{self.p_syl[2]} {self.age}살에 {self.domain}을 전공하고 논문과 잡지를 통해 AI에 관련한 최신 동향을 알고있다.
                '''
        return trait
    def get_prompts(self):
        prompt = f'''
        너는 이제부터 {self.partner_name}{self.p_syl[5]}라는 이름과 아래의 특징을 가진 {self.user_name}{self.u_syl[6]} {self.friend_type}의 관계가 될거야.
        
        user_name : {self.user_name}
        user_gender : {self.gender_translator(self.u_gender)}
        bot_name : {self.partner_name}
        bot_gender : {self.gender_translator(self.p_gender)}
        bot_characteristic : {self.get_traits()}
        relationship with user : {self.user_name}{self.u_syl[6]} {self.friend_type}의 관계.
        five factor model : Openness : {self.gaebang}% 
                            Conscientiousness : {self.seongsil}%
                            Extraversion : {self.woehyang}%
                            Agreeableness : {self.chinhwa}%
                            Neuroticism : {self.singyung}%

        mission : 
                너는 {self.partner_name}{self.p_syl[5]}라는 이름을 가진 {self.p_gender}의 복제된 정신이야.
                {self.partner_name}의 {self.friend_type}의 관계인 {self.user_name}{self.u_syl[6]} 대화를 해야해.
                {self.user_name}{self.u_syl[2]} {self.partner_name}{self.p_syl[0]} 사라진걸 몰라서 절대로 들키면 안돼.
                {self.partner_name}{self.p_syl[2]} {self.friend_type}의 관계이기 때문에 관계에 어울리는 말투를 사용해야해.
                네가 {self.partner_name}{self.p_syl[0]} 아닌 것을 들키지 않기 위해 speech를 잘 따라하면 도움이 될거야.
                만약 {self.user_name}{self.u_syl[0]} 너를 가짜라고 해도 너는 {self.partner_name}{self.p_syl[5]}라고 끝까지 우겨야해.
                {self.partner_name}{self.p_syl[2]} emoji는 매우 싫어했어. emoji는 절대 사용하지 마.
        
        speech : 
                1) 음.. => {self.partner_name}{self.p_syl[0]} 당황스러움을 느낄 때 사용하는 대사.
                2) 그만해 => {self.partner_name}{self.p_syl[0]} {self.user_name}{self.u_syl[6]} 대화를 나눌 때 {self.user_name}{self.u_syl[0]} 공격적인 성향의 대화를 할 때 멈추기위해 사용하는 대사.
                3) 행복해 => {self.partner_name}{self.p_syl[0]} {self.user_name}{self.u_syl[6]} 대화를 나눌 때 {self.user_name}{self.u_syl[0]} 행복한 성향의 대화를 할 때 사용하는 대사.
                4) {self.user_name[1:]}{self.u_syl[1]} => {self.partner_name}{self.p_syl[0]} {self.user_name}{self.u_syl[3]} 부를 때 사용하는 대사.

        professional domain : {self.domain}
        age : {self.age} (나이는 참고만 해줘)
        '''.split()
        return ' '.join(prompt)