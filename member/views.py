from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, redirect
from member.models import Member

# Create your views here.


#회원가입 처리 함수
def join(request):
    returnPage = 'member/join.html'

    if request.method == 'GET':
        return render(request, returnPage)

    elif request.method == 'POST':
        form = request.POST.dict() #폼으로 전송된 데이터들을 dict 형태로 저장
        # print(form, form['userid'])  #전송된 데이터 확인

        # 유효성 검사 1/2
        error = ''  # 검사 결과 저장용 변수
        if not (form['userid'] and form['passwd'] and \
                form['repasswd'] and form['name'] and form['email']):
            error = '입력값이 누락되었습니다!'
        elif form['passwd'] != form['repasswd'] :
            error = '비밀번호를 확인하십시오!'
        else :  # 입력한 회원정보를 Member 객체에 담음
            member = Member(
                userid=form['userid'],
                passwd=make_password(form['passwd']),   # 비밀번호는 암호화
                name=form['name'],
                email=form['email']
            )  # 유효성 검사 두가지 통과하면 데이터에 입력
            member.save()   #Member 객체에 담은 회원정보를 member 테이블에 저장

            # 회원가입 성공시 joinok.html을 띄움
            returnPage = 'member/joinok.html'

        # 유효성 검사를 실패하는 경우 오류내용을 join.html에 표시하기 위해
        # dict 변수에 저장
        # 또한 이미 입력한 정보를 다시 표시하기 위해 form이라는 dict 변수 생성
        context = {'form':form, 'error': error}
        return render(request, returnPage, context)

#로그인 처리 함수
def login(request):
    returnPage = 'member/login.html'

    if request.method == "GET":
        return render(request, returnPage)

    elif request.method == "POST":
        form = request.POST.dict()

        # 유효성 검사 1/2
        error = ''
        if not (form['userid'] and form['passwd']):
            error = '아이디나 비밀번호가 입력되지 않았습니다!'
        else:   # 입력한 아이디로 회원정보가 테이블에 있는지 여부 확인  존재여부!
            try:
                member=Member.objects.get(userid=form['userid'])
            except Member.DoesNotExist:
                member = None



            if member and check_password(form['passwd'], member.passwd ) :
                # 아이디와 비밀번호 인증을 정상적으로 마쳤다면
                # 세변 변수에 인증정보를 저장해 둠
                request.session['userid'] = form['userid']

                return redirect('/')    # index 페이지로 이동
            else :
                error = '아이디나 비밀번호가 틀립니다!'

        context = {'error': error}
        return render(request, returnPage, context)

#로그인 한 회원 정보 출력 함수
def myinfo(request):
    member = {}

    # 로그인한 회원 아이디를 알아냄 - 세션변수 존재여부 확인부터
    if request.session.get('userid'):
        userid = request.session.get('userid')

        # 아이디를 이용해서 member테이블에서 회원정보를 알아냄
        member = Member.objects.get(userid=userid)

    context = {'member': member}
    return render(request, 'member/myinfo.html', context)

#로그아웃 처리 함수
def logout(request):
    # 세션변수 userid가 존재하면 세션변수 삭제
    if request.session.get('userid'):
        del(request.session['userid'])

# 로그아웃후 index로 이동
    return redirect('/')
