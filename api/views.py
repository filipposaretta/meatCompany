from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Lot, Ip, Wal
from django.http import JsonResponse
from django.utils import timezone
from .forms import PostForm, Lotto, Wallet
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from api.utils import sendTransaction
from django.db.models import Q
import hashlib
import datetime

def posts(request):  #if we want a Json response
    response = []
    posts = Post.objects.filter().order_by('datetime')
    for post in posts:
        response.append(
            {
                'published_date': post.published_date,
                'content': post.content,
                'author': f"{post.user.first_name} {post.user.last_name}",
                'hash': post.hash,
                'txId': post.txId,
            }
        )
    return JsonResponse(response, safe=False)

def post_list(request):  #this is public
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'api/post_list.html', {'posts':posts})

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'api/post_detail.html', {'post': post})

@login_required
def post_new(request):  #private and hash content
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.hash = hashlib.sha256(post.content.encode('utf-8')).hexdigest()
            post.save()
            messages.add_message(request, messages.INFO, 'Form saved.')
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'api/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):  #edit of the post
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            messages.add_message(request, messages.INFO, 'Form saved.')
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'api/post_edit.html', {'form': form})

@login_required
def post_remove(request,pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

def login(request):
    if request.user.is_authenticated:
        return redirect('admin')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            # correct username and password login the user
            auth.login(request, user)
            return redirect('user_details')
        else:
            messages.error(request, 'Error wrong username/password')

    return render(request, 'api/login.html')

@login_required
def logout(request):
    auth.logout(request)
    return render(request,'api/logout.html')

@login_required
def user_details(request):
    user = get_object_or_404(User, id=request.user.id)

    #if we have a super user we check the ip
    for x in range(User.objects.filter(is_superuser=True).count()):
        if User.objects.filter(is_superuser=True)[x].username == request.user.username:
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

            if x_forwarded_for:
                ipaddress = x_forwarded_for.split(',')[-1].strip()
            else:
                ipaddress = request.META.get('REMOTE_ADDR')

            get_ip = Ip() #imported class from model
            get_ip.ip_address= ipaddress
            get_ip.pub_date = datetime.date.today() #import datetime
            get_ip.change = False
            if ipaddress != Ip.objects.latest('pub_date').ip_address:
                get_ip.change = True
            get_ip.save()

            return render(request, 'api/user_details.html', {'user': user, 'get_ip': get_ip})
    return render(request, 'api/user_details.html', {'user': user, 'get_ip': ''})

def signup(request):
    if request.user.is_authenticated:
        return redirect('user_details', username=request.user.username)

    if request.method == 'POST':
        f = UserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            messages.success(request, 'Account created successfully')
            return redirect('signup')
    else:
        f = UserCreationForm()
    return render(request, 'api/signup.html', {'form': f})

# lots from here

def lots(request):  #only this and search are public
    response = []
    lots = Lot.objects.filter().order_by('lot')
    for lot in lots:
        response.append(
            {
                'lot': lot.lot,
                'id_code': lot.id_code,
                'description': lot.description,
                'published_date': lot.published_date,
                'addr': lot.addr,
                'pr_k': lot.pr_k,
            }
        )
    return JsonResponse(response, safe=False)

@login_required
def lot_list(request):
    for x in range(User.objects.filter(is_superuser=True).count()):
        if User.objects.filter(is_superuser=True)[x].username == request.user.username:
            lots = Lot.objects.filter(published_date__lte=timezone.now()).order_by('lot')
            return render(request, 'api/lot_list.html', {'lots':lots})
    return render(request,'api/wrong_user.html')

@login_required
def lot_detail(request, pk):
    for x in range(User.objects.filter(is_superuser=True).count()):
        if User.objects.filter(is_superuser=True)[x].username == request.user.username:
            lot = get_object_or_404(Lot, pk=pk)
            return render(request, 'api/lot_detail.html', {'lot':lot})
    return render(request,'api/wrong_user.html')


@login_required
def lot_new(request):
    for x in range(User.objects.filter(is_superuser=True).count()):
        if User.objects.filter(is_superuser=True)[x].username == request.user.username:
            if request.method == "POST":
                form = Lotto(request.POST)
                if form.is_valid():
                    lot = form.save(commit=False)
                    lot.published_date = timezone.now()
                    lot.save()
                    messages.add_message(request, messages.INFO, 'Lot saved.')
                    return redirect('lot_detail', pk=lot.pk)
            else:
                form = Lotto()
            return render(request, 'api/lot_edit.html', {'form': form})
    return render(request,'api/wrong_user.html')

@login_required
def lot_edit(request, pk):
    for x in range(User.objects.filter(is_superuser=True).count()):
        if User.objects.filter(is_superuser=True)[x].username == request.user.username:
            lot = get_object_or_404(Lot, pk=pk)
            if request.method == "POST":
                form = Lotto(request.POST, instance=lot)
                if form.is_valid():
                    lot = form.save(commit=False)
                    lot.published_date = timezone.now()
                    lot.save()
                    messages.add_message(request, messages.INFO, 'Form saved.')
                    return redirect('lot_detail', pk=lot.pk)
            else:
                form = Lotto(instance=lot)
            return render(request, 'api/lot_edit.html', {'form': form})
    return render(request,'api/wrong_user.html')

@login_required
def lot_remove(request,pk):
    for x in range(User.objects.filter(is_superuser=True).count()):
        if User.objects.filter(is_superuser=True)[x].username == request.user.username:
            lot = get_object_or_404(Lot, pk=pk)
            lot.delete()
            return redirect('lot_list')
    return render(request,'api/wrong_user.html')

@login_required
def wrong_user(request):
    return render(request, 'api/wrong_user.html')

def search(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        submitbutton = request.GET.get('submit')
        error = False
        #if the query is not empty
        if query is not None:
            lookups= Q(lot__icontains=query) | Q(id_code__icontains=query)
            results= Lot.objects.filter(lookups).distinct()
            try:
                transition = results[0].lot + results[0].description
                transition_hash = hashlib.sha256(transition.encode('utf-8')).hexdigest()
            except IndexError:
                transition_hash = "Search not found"
            trans_txId = ""
            if request.user.is_authenticated:
                if Wal.objects.count() > 0:  #if there are wallets
                    try:  #tmp_wal conteins the right wallet
                        tmp_wal = Wal.objects.filter(author = request.user.username)[0]
                        try:  #check if Ethereum test are available
                            trans_txId = sendTransaction(transition_hash, tmp_wal.ropsten, tmp_wal.address, tmp_wal.private_key)
                        except ValueError:
                            trans_txId = "You have no Ethereum"
                            error = True
                    except IndexError:
                        trans_txId = "You don't have a wallet!"
                        error = True
                else:
                    trans_txId = "You don't have a wallet. Create one!"
                    error = True

            context={'results': results,
                     'submitbutton': submitbutton,
                     'trans_txId': trans_txId,
                     'error': error}
            return render(request, 'api/search.html', context)
        else:
            return render(request, 'api/search.html')
    else:
        return render(request, 'api/search.html')

@login_required
def wallet(request):
    if request.method == "POST":
        form = Wallet(request.POST)
        if form.is_valid():
            wal = form.save(commit=False)
            if not wal.new_wallet:  #if the wallet is old
                wal.author = request.user.username
                wal.save()
                messages.add_message(request, messages.INFO, 'Wallet saved.')
                return redirect('lot_list')
            else:  #if the wallet is new
                w3 = Web3(Web3.HTTPProvider(wal.ropsten))
                account = w3.eth.account.create()
                wal.author = request.user.username
                wal.private_key = account.privateKey.hex()
                wal.address = account.address
                wal.save()
                messages.add_message(request, messages.INFO, 'Wallet saved.')
                return redirect('lot_list')
    else:
        form = Wallet()
    return render(request, 'api/wallet.html', {'wal': form})