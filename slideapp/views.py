from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import os
import uuid
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
import os
import uuid
from django.conf import settings
from imghdr import what

from django.shortcuts import render, redirect
from .models import Slide
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

@csrf_exempt
@login_required
def upload_image(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        if image and image.content_type.startswith('image/'):
            # 生成唯一的文件名，防止冲突
            ext = os.path.splitext(image.name)[1]
            filename = uuid.uuid4().hex + ext
            filepath = os.path.join(settings.MEDIA_ROOT, 'uploads', filename)

            # 确保上传目录存在
            os.makedirs(os.path.dirname(filepath), exist_ok=True)

            # 保存文件
            with open(filepath, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)

            # 返回图片的访问 URL
            url = settings.MEDIA_URL + 'uploads/' + filename
            return JsonResponse({'url': url})
        else:
            return JsonResponse({'error': '无效的文件'}, status=400)
    else:
        return JsonResponse({'error': '不支持的请求方法'}, status=405)





# slideapp/views.py
@login_required
@csrf_exempt
def index(request):
    # 按照创建时间排序的幻灯片
    slides = Slide.objects.all().order_by('-created_at')  # 按照创建时间降序排序
    return render(request, 'index.html', {'slides': slides})

@login_required
@csrf_exempt
def create_slide(request):
    slide = Slide.objects.create()
    return redirect('edit_slide', slide_id=slide.id)

@login_required
@csrf_exempt
def edit_slide(request, slide_id):
    slide = Slide.objects.get(id=slide_id)
    return render(request, 'edit_slide.html', {'slide': slide})

@login_required
@csrf_exempt
def delete_slide(request, slide_id):
    slide = get_object_or_404(Slide, id=slide_id)
    slide.delete()
    return JsonResponse({'status': 'success'})

@login_required
@require_POST
@csrf_exempt
def toggle_lock(request, slide_id):
    slide = get_object_or_404(Slide, id=slide_id)
    # 切换锁定状态
    slide.lock = not slide.lock
    slide.save()
    return JsonResponse({'status': 'success', 'lock': slide.lock})


@csrf_exempt
def public_slides(request):
    slides = Slide.objects.filter(lock=False).order_by('-created_at')
    return render(request, 'public_slides.html', {'slides': slides})

@csrf_exempt
def public_edit_slide(request, slide_id):
    slide = get_object_or_404(Slide, id=slide_id, lock=False)
    return render(request, 'public_edit_slide.html', {'slide': slide})