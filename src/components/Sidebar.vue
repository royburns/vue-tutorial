<template>
    <div class="card">
        <div v-if="is_login" class="card-header" align="center">
            <img src="http://avatar.csdn.net/1/E/E/1_kevin_qq.jpg"
                 class="avatar img-circle img-responsive" />
            <p><strong v-text="username"></strong>
                <a href="javascript:" @click="logout()" title="退出登录">
                    <i class="fa fa-sign-out float-xs-right"></i></a>
            </p>
            <p>
            <a href="javascript:" class="card-title nav-link" @click="getSubscription()">
            <i class="fa fa-arrow-circle-down" title="下载列表"></i></a>
    			订阅列表 
            <a href="javascript:" class="card-title nav-link" @click="uploadSubscription()">
            <i class="fa fa-arrow-circle-up" title="上传列表"></i></a>
            </p>  	
        </div>
        <div v-else class="card-header" align="center">
            <form class="form" @submit.prevent>
                <div class="form-group">
                    <input class="form-control" name="username" type="email" placeholder="name@example.com" v-model="username"
                           required pattern="\w+?@\w+?\.\w+$" />
                           <p class="text-muted"><small>请输入有效的Email地址</small></p>
                </div>
                <div class="form-group">
                    <input class="form-control" name= "password" type="password" placeholder="密码" v-model="password"
                           required pattern="\w{6,}"/>
                           <p class="text-muted"><small>密码至少6位，字母数字下划线</small></p>
                </div>
                <div class="form-group clearfix">
                    <input type="submit" @click="register()" class="btn btn-outline-danger float-xs-left" 
                    	value="注册" :disabled="!validation" />
                    <input type="submit" @click="login()" class="btn btn-outline-success float-xs-right" 
                    	value="登录" :disabled="!validation" />
                </div>
            </form>
            <a href="javascript:" class="card-title nav-link" @click="getSubscription()">订阅列表</a>
        </div>
        <div class="card-block">
            <p v-for="(mp, idx) in subscribeList" @mouseover="showRemove(idx)" @mouseout="hideRemove(idx)">
                <small>
    				<a href="javascript:" class="nav-link" @click="fetchArticles(mp.weixinhao, mp.mpName)" title="获取服务器上文章列表">
    					<img :src="mp.image" class="mpavatar img-circle img-responsive" /> {{ mp.mpName }} </a>
    				<i :class="{'fa fa-spinner fa-spin fa-lg fa-fw': isFetching}"></i>
                    <a href="javascript:" @click="unsubscribeMp(mp.weixinhao)">
                        <i class="fa fa-lg float-xs-right text-danger sidebar-remove"
                           :class="{'fa-minus-circle': mp.showRemoveBtn}"></i></a></small>

            </p>
        </div>
    </div>
</template>

<script>
    export default {
        name: 'Sidebar',
        data() {
            return {
                is_login: false,
                username: '',
                password: '',
                token: '',
                	isFetching: false,
            }
        },
        created: function() {
      //  	window.localStorage.setItem("isFetching", false);
            // 从LocalStorage中取出数据
            if (window.localStorage.getItem("user")) {
                var userData = JSON.parse(window.localStorage.getItem("user"));
                this.token = userData.token;
                this.username = userData.username;
                this.is_login = true
            }
            return this.$store.dispatch('initFromLS', 'init from LS');
        },
        computed: {
            subscribeList() {
                // 从store中取出数据
                return this.$store.state.subscribeList
            },
            validation() {
                var patt1 = /(\w+?@\w+?\.\w+$)/;
                var patt2 = /(\w{6,})/;
                //            	alert(this.username + patt1.test(this.username));
                return (this.username=='admin' || patt1.test(this.username)) && patt2.test(this.password)
            }
        },
        methods: {
        	fetchArticles(weixinhao, mpName){
//        		return this.$router.push({ name: 'article', params: { id: weixinhao }})
            this.isFetching = true;
            this.$nextTick(function () { });
            this.$http.get('/api/v1.0/articles', {
                    params: {
                        email: this.username,
                        	weixinhao: weixinhao
                    },
                    headers: {
                        'Content-Type': 'application/json; charset=UTF-8',
                        'Authentication-Token': this.token
                    }
                }).then((response) => {
                    // 响应成功回调
    			this.isFetching = false;
    			this.$nextTick(function () { });
                   var data = response.body, article_data;
                    if (!data.status == 'ok') {
 //                   return alert('文章 from server：\n' + JSON.stringify(data));
 				return alert('获取失败，请重新上传订阅列表！\n' +data.status)
                	}
     		article_data = {
     			'mpName': mpName,
     			'weixinhao': weixinhao,
     			'articles': data.articles,
     			'sync_time': data.sync_time
     			}
			window.localStorage.setItem('weixinhao_'+weixinhao, JSON.stringify(article_data));
			// 必须要命名route name，否则，地址会不停地往后加 /article/XXX, /article/article/XXX
			return this.$router.push({ name: 'article', params: { id: weixinhao, mpName: mpName }})
                }, (response) => {
                    // 响应错误回调
                    alert('同步出错了！ ' + JSON.stringify(response))
                    if (response.status == 401) {
                        alert('登录超时，请重新登录');
                        this.is_login = false;
                        this.password = '';
                        window.localStorage.removeItem("user")
                    }
                });
            },
            unsubscribeMp(weixinhao) {
                // 删除该公众号
                return this.$store.dispatch('unsubscribeMp', weixinhao);
            },
            showRemove(idx) {
                return this.subscribeList[idx]['showRemoveBtn'] = true;
            },
            hideRemove(idx) {
                return this.subscribeList[idx]['showRemoveBtn'] = false;
            },
            login() {
                //            this.$http.options.headers={
                //'Content-Type':'application/json; charset=UTF-8'
                //};
                if (!this.validation) return;
                // get CSRF
                var csrf_token = '';
                this.$http.get('/login').then((response) => {
                    // 响应成功回调
                    var data = response.body;
                    //                 alert(JSON.stringify(response));
                    // <input id="csrf_token" name="csrf_token" type="hidden" value="1483433916##5b057abdef66da070c8385752b78f6c584f6ba41"><input
                    var csrf_token = '';
                    try {
                        csrf_token = data.match(/name="csrf_token" type="hidden" value="(.*?)">/)[1];
                        //                	alert(csrf_token);
                    } catch (exception) {
                        // 如果已经登陆，则302，redirect to home
                        //               	alert(exception);	// exception: TypeError: Cannot read property '1' of null
                        alert('登录异常，请重新登录');
                        return window.location = '/logout';
                    }
                    this.$http.post('/login',
                        //body
                        {
                            email: this.username,
                            password: this.password,
                            csrf_token: csrf_token
                        },
                        //options
                        {
                            headers: {
                                'Content-Type': 'application/json; charset=UTF-8'
                            }
                        }).then((response) => {
                        // 响应成功回调
                        var jsondata = response.body;
                        alert('登录成功！\n' + JSON.stringify(jsondata));
                        this.token = jsondata.response.user.authentication_token;
                        this.is_login = true;
                        //               alert('token:\n'+ this.token);
                        var userData = {
                            'username': this.username,
                            'token': this.token
                        };
                        window.localStorage.setItem("user", JSON.stringify(userData));
                        //     this.$nextTick(function () { });
                        //   getSubscription()
                    }, (response) => {
                        // 响应Login-POST错误回调
                        alert('登录出错了！ ' + response.status + response.statusText)
                    });
                }, (response) => {
                    // 响应login-GET 错误回调
                    alert('登录出错了(CSRF)！ ' + JSON.stringify(response))
                });
            },
            register() {
                if (!this.validation) return;
                // get CSRF
                var csrf_token = '';
                this.$http.get('/register').then((response) => {
                    // 响应成功回调
                    var data = response.body;
                    // <input id="csrf_token" name="csrf_token" type="hidden" value="1483433916##5b057abdef66da070c8385752b78f6c584f6ba41"><input
                    var csrf_token = data.match(/name="csrf_token" type="hidden" value="(.*?)">/)[1]
                    //          	alert(csrf_token);                
                    this.$http.post('/register',
                        //body
                        {
                            email: this.username,
                            password: this.password,
                            csrf_token: csrf_token
                        },
                        //options
                        {
                            //             emulateHTTP: true,
                            headers: {
                                'Content-Type': 'application/json; charset=UTF-8'
                            }
                        }).then((response) => {
                        // 响应成功回调
                        var data = response.body;
                        //          alert('Server rsp:\n'+ JSON.stringify(response));
                        //"body":{"meta":{"code":400},"response":{"errors":{"email":["aaa@bbb.com is already associated with an account."]}}},
                        if (data.meta.code !== 200) {
                            return alert(JSON.stringify(data.response.errors))
                        }
                        this.token = data.response.user.authentication_token;
                        this.is_login = true;
                        //            alert(this.token);
                        var userData = {
                            'username': this.username,
                            'token': this.token
                        };
                        window.localStorage.setItem("user", JSON.stringify(userData));
                    }, (response) => {
                        // 响应错误回调
                        alert('注册出错了！ ' + JSON.stringify(response))
                    });
                }, (response) => {
                    // 响应register-GET 错误回调
                    alert('注册出错了(CSRF)！ ' + JSON.stringify(response))
                });
            },
            logout() {
                this.$http.get('/logout').then((response) => {
                    // 响应成功回调
                    this.is_login = false;
                    this.password = '';
                    this.token = '';
                    window.localStorage.removeItem("user")
                }, (response) => {
                    // 响应错误回调
                    alert('Logout出错了！ ' + JSON.stringify(response))
                });
            },
            uploadSubscription() {
                if (this.subscribeList.length === 0) return false;
                this.$http.post('/api/v1.0/mps',
                    //body
                    {
                        email: this.username,
                        mps: this.subscribeList
                    },
                    //options
                    {
                        headers: {
                            'Content-Type': 'application/json; charset=UTF-8',
                            'Authentication-Token': this.token
                        }
                    }).then((response) => {
                    // 响应成功回调
                    var data = response.body,
                        mp;
                    alert('成功上传订阅号：\n' + JSON.stringify(data))

                }, (response) => {
                    // 响应错误回调
                    alert('同步出错了！ ' + JSON.stringify(response))
                    if (response.status == 401) {
                        alert('登录超时，请重新登录');
                        this.is_login = false;
                        this.password = '';
                        window.localStorage.removeItem("user")
                    }
                });
            },
            getSubscription() {
                this.$http.get('/api/v1.0/mps', {
                    params: {
                        email: this.username
                    },
                    headers: {
                        'Content-Type': 'application/json; charset=UTF-8',
                        'Authentication-Token': this.token
                    }
                }).then((response) => {
                    // 响应成功回调
                    var data = response.body,
                        mp, found_tag = false;
                    alert('订阅号 from server：\n' + JSON.stringify(data));
                    // [{"articles_count":2,"image":null,"summary":null,"weixinhao":"aaa"},{"articles_count":0,"image":null,"summary":null,"weixinhao":"bbb"}]
                    //                 this.$store.dispatch('clearSearchResult', 'clear search result');
                    for (let item of this.subscribeList) {
                        this.$store.dispatch('unsubscribeMp', item.weixinhao);
                    }
                    this.$store.dispatch('clearSubscription', 'get sublist from Server');
                    for (let mp of data) {
                        //  	    for(let item of this.subscribeList) {
                        // 如果已经订阅，则跳过
                        //	if(item.weixinhao == mp.weixinhao) { found_tag = true}
                        //    }
                        //  	if (! found_tag) {
                        mp['showRemoveBtn'] = false;
                        this.$store.dispatch('subscribeMp', mp);
                        //	found_tag = false
                        //	}
                    }
                }, (response) => {
                    // 响应错误回调
                    alert('同步出错了！ ' + JSON.stringify(response))
                    if (response.status == 401) {
                        alert('登录超时，请重新登录');
                        this.is_login = false;
                        this.password = '';
                        window.localStorage.removeItem("user")
                    }
                });
            }
        }
    }
</script>

<style>
    .avatar {
        height: 75px;
        margin: 0 auto;
        margin-top: 10px;
        margin-bottom: 10px;
    }
    
    .mpavatar {
        height: 30px;
        margin: 0 auto;
        margin-top: 2px;
        margin-bottom: 2px;
    }
    
    .img-circle {
        border-radius: 50%;
    }
    
    .sidebar-remove {
        margin-top: 8px;
    }
</style>