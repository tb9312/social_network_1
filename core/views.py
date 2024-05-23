from itertools import chain
from random import shuffle
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from .models import Post,Profile,Like,Follow,Comment,Comment_liked_by_user,Notification
from .forms import PostForm
from django.db.models import Q

# Create your views here.
def signIn(request):
    title = 'Sign In - Ishare'
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('homePage')
        else:
            messages.info(request,'Invalid Credentials')
            return redirect('signIn')
        


    else:
        return render(request,'core/signIn.html',{'title': title})

def signUp(request):
    title = 'Sign Up - Ishare'
    if request.method=='POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'User Name Taken')
                return redirect('signUp')
            else:

                user = User.objects.create_user(username=username,first_name=fname,last_name=lname,password=password)
                user.save()

                # create profile for user
                user_model = User.objects.get(username=username)
                profile = Profile.objects.create(user=user_model)
                profile.save()
                # messages.success(request,'Account created successfully')
                return redirect('signIn')
        else:
            messages.info(request,'Password Not Matching')
            return redirect('signUp')
    else:
        return render(request, 'core/signUp.html',{'title': title})

@login_required(login_url='signIn')   
def logOut(request):
    auth.logout(request)
    return redirect('signIn')
    
@login_required(login_url='signIn')
def homePage(request):
    title = 'Home - Ishare'

    user_object = request.user
    user_profile = Profile.objects.get(user=user_object) 

    # feed list
    feed=[]
    posts = Post.objects.filter(user_id=user_object)
    feed.append(posts)

    users_following = Follow.objects.filter(user=user_object)
    for user in users_following:
        post=Post.objects.filter(user_id=user.following_user_id)
        feed.append(post)
    feed_list=list(chain(*feed))

    feed_list = sorted(feed_list, key=lambda x: x.create_at)

    # suggest user
    all_user=User.objects.all()
    all_user_following = []
    all_user_following.append(user_object)
    for user in users_following:
        user_list=User.objects.get(username=user.following_user_id.username)
        all_user_following.append(user_list)
    suggestion_list=[x for x in list(all_user) if (x not in list(all_user_following)) and x.username!='admin']
    shuffle(suggestion_list)
    
    # upload post
    if request.method=='POST':
        image_url = request.POST['image_url']
        caption = request.POST['caption']
        location = request.POST['location']
        # print(image_url)
        post = Post.objects.create(image=image_url, caption=caption, location=location,user_id=request.user)
        post.save()
        return redirect('homePage')
    return render(request,'core/homePage.html',{'title': title,'user':user_profile,'posts':feed_list,'suggestion_list':suggestion_list})

@login_required(login_url='signIn')
def likePost(request):
    username = request.user.username
    post_id = request.GET['post_id']
    post = Post.objects.get(post_id=post_id)

    like_filter = Like.objects.filter(username=username, post_id=post_id).first()

    if like_filter == None:
        like = Like.objects.create(username=username, post_id=post_id)
        like.save()

        if post.user_id!=request.user:
            description = ''.join(post.caption[:40])
            description+='...'

            notification = Notification.objects.create(user_id=post.user_id,user_create=request.user,type='liked your post',link='/comment/'+post_id,description=description)
            notification.save()

        post.no_of_like+=1
        post.save()

        return JsonResponse({'success': True, 'like_count': post.no_of_like})
    else:
        like_filter.delete()
        post.no_of_like-=1
        post.save()

        return JsonResponse({'success': True, 'like_count': post.no_of_like})

@login_required(login_url='signIn')
def likeComment(request):
    user=request.user
    
    comment_id=request.GET['comment_id']
    comment = Comment.objects.get(comment_id=comment_id)
    post_id=comment.post_id.post_id

    like_comment = Comment_liked_by_user.objects.filter(comment_id=comment,user_id=user).first()

    if like_comment ==None:
        like = Comment_liked_by_user.objects.create(comment_id=comment,user_id=user)
        like.save()

        if comment.user_id!=request.user:
            description = ''.join(comment.content[:40])
            description+='...'

            notification = Notification.objects.create(user_id=comment.user_id,user_create=request.user,type='liked your comment',link='/comment/'+post_id,description=description)
            notification.save()
        

        comment.no_of_like+=1
        comment.save()

        return JsonResponse({'success': True, 'like_count': comment.no_of_like})
    else:
        like_comment.delete()
        comment.no_of_like-=1
        comment.save()

        return JsonResponse({'success': True, 'like_count': comment.no_of_like})

@login_required(login_url='signIn')
def follow(request):
    user_model_id=request.GET['user_id']
    user_model=User.objects.get(id=user_model_id)
    user_profile = Profile.objects.get(user=user_model)

    user_model_now = request.user
    user_profile_now = Profile.objects.get(user=user_model_now)

    follow_filter = Follow.objects.filter(user=user_model_now,following_user_id=user_model).first()

    if follow_filter==None:
        follow = Follow.objects.create(user=user_model_now,following_user_id=user_model)
        follow.save()

        notification=Notification.objects.create(user_create=user_model_now,user_id=user_model,link='/profile/'+user_model_now.username,type='followed you')
        notification.save()

        user_profile_now.no_of_following+=1
        user_profile_now.save()

        user_profile.no_of_followed+=1
        user_profile.save()
        return redirect('/profile/'+user_model.username)
    else:
        follow_filter.delete()

        notification=Notification.objects.create(user_create=user_model_now,user_id=user_model,link='/profile/'+user_model.username,type='unfollowed you')
        notification.save()

        user_profile_now.no_of_following-=1
        user_profile_now.save()

        user_profile.no_of_followed-=1
        user_profile.save()
        return redirect('/profile/'+user_model.username)

@login_required(login_url='signIn')
def profile(request,pk):
    title = 'Profile - Ishare'
    user_model=User.objects.get(username=pk)
    user_profile=Profile.objects.get(user=user_model)
    posts = Post.objects.filter(user_id=user_model)
    user_model_now = request.user
    user_profile_now = Profile.objects.get(user=user_model_now)

    is_following = Follow.objects.filter(user=user_model_now,following_user_id=user_model).exists()
    return render(request,'core/profile.html',{'title':title,'user_profile':user_profile,'posts':posts,'user':user_profile_now,'is_following':is_following})

@login_required(login_url='signIn')
def editProfile(request):
    title = 'Edit Profile - Ishare'
    user_model = User.objects.get(username = request.user.username)
    user_profile = Profile.objects.get(user=user_model)

    if request.method=='POST':
        image = request.POST['image_url']
        if image:
            user_profile.image=image
        user_model.first_name = request.POST['fname']
        user_model.last_name = request.POST['lname']
        user_profile.website = request.POST['website']
        user_profile.bio = request.POST['bio']

        user_profile.save()
        user_model.save()
        return redirect('/profile/'+user_model.username)
        

    return render(request,'core/editProfile.html',{'title':title,'user':user_profile})

@login_required(login_url='signIn')
def comment(request,id):
    user_model=request.user
    post_id=id
    post=Post.objects.get(post_id=post_id)
    comments=Comment.objects.filter(post_id=post)

    if request.method=='POST':
        comment_content=request.POST['postcmt']
        comment=Comment.objects.create(content=comment_content,post_id=post,user_id=user_model)
        comment.save()
        description = ''.join(comment_content[:40])
        description+='...'
        notification=Notification.objects.create(user_id=post.user_id,user_create=user_model,link='/comment/'+post_id,type='commented your post',description=description)
        notification.save()
        return redirect('/comment/'+post_id)
    
    return render(request,'core/comment.html',{'post':post,'comments':comments})

@login_required(login_url='signIn')
def notification(request):
    title = 'Notifications - Ishare'

    user_object=request.user
    user_profile = Profile.objects.get(user=user_object)
    new,seen=[],[]
    seen_notif = Notification.objects.filter(user_id=user_object, is_read=True)
    new_notif = Notification.objects.filter(user_id=user_object, is_read=False)
    new.append(new_notif)
    seen.append(seen_notif)
    new_list=list(chain(*new))
    seen_list=list(chain(*seen))
    for notif in new_list:
        notif.is_read = True
        notif.save()

    return render(request,'core/notification.html',{'title':title,'user':user_profile,'news':new_list,'seens':seen_list})

@login_required(login_url='signIn')
def search(request):
    title = 'Edit Profile - Ishare'

    user_object=request.user
    user_profile = Profile.objects.get(user=user_object)

    users=User.objects.all()

    return render(request,'core/search.html',{'title':title,'user':user_profile,'users':users})



# @login_required(login_url='signIn')
# def createPost(request):
#     if request.method=='POST':
#         image_url = request.POST['image_url']
#         caption = request.POST['caption']
#         location = request.POST['location']
#         # print(image_url)
#         post = Post.objects.create(image=image_url, caption=caption, location=location,user_id=request.user)
#         post.save()
#         return redirect('homePage')
#     return render(request,'core/createPost.html')