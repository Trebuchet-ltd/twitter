from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, get_object_or_404, redirect

from home.models import Assessment, Response, Answer, Result


def index(request):
    return render(request, 'home/index.html', context={})


def try_saving_response(request: WSGIRequest, resp: Response):
    for i, question in enumerate(resp.current_page.questions.all()):
        query = f'{question.id}[]' if question.category == 'ms' else f'{question.id}'
        answer = ",".join(request.POST.getlist(query))

        if question.category == 'tf':
            answer = answer == 'true'

        if not answer:
            raise ValueError(f'Question {i+1} was not answered')

        ans = Answer.objects.get_or_create(question=question, response=resp)[0]
        ans.answer_text = answer
        ans.save()

    if resp.current_page == resp.assessment.formpage_set.last():
        resp.current_page = None
    else:
        resp.current_page = resp.assessment.formpage_set.filter(id__gt=resp.current_page.id).first()

    resp.save()

    return resp


def assessment(request, assessment_id, response_id):
    obj = get_object_or_404(Assessment, id=assessment_id)

    if response_id == -1:
        resp = Response(assessment=obj)
        resp.current_page = obj.formpage_set.first()
        resp.save()

        return redirect('assessment', assessment_id=obj.id, response_id=resp.id)

    resp = get_object_or_404(Response, id=response_id)

    error = None
    if request.method == 'POST' and resp.current_page is not None:
        try:
            resp = try_saving_response(request, resp)
        except ValueError as e:
            error = str(e)

    if resp.current_page is None:
        return redirect('result', response_id=resp.id)

    page_titles = [page.name for page in obj.formpage_set.all()]
    title = resp.current_page.title
    page_index = page_titles.index(resp.current_page.name)
    description = resp.current_page.description
    questions = resp.current_page.questions.all()

    context = {
        'id': resp.id,
        'page_index': page_index,
        'num_titles': len(page_titles) + 1,
        'titles': page_titles,
        'page_title': title,
        'description': description,
        'questions': questions,
        'error': error
    }

    return render(request, 'home/assessment.html', context=context)


def assessments(request):
    objs = Assessment.objects.all()
    return render(request, 'home/assessments.html', context={"assessments": objs})


def result(request, response_id):
    resp = get_object_or_404(Response, id=response_id)
    result_data = Result.objects.get_or_create(response=resp)[0]
    result_pages = result_data.resultpage_set.all()

    context = {
        'result': result_data,
        'pages': result_pages
    }

    return render(request, 'home/result.html', context=context)
