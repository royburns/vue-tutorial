<template>
    <div class="card">
        <div v-if="is_login" class="card-header" align="center">
            <img src="http://avatar.csdn.net/1/E/E/1_kevin_qq.jpg"
                 class="avatar img-circle img-responsive" />
            <p><strong v-text="username"></strong>
                <a href="javascript:" @click="logout()" title="退出">
                    <i class="fa fa-sign-out float-xs-right"></i></a>
            </p>
            <a href="javascript:" class="card-title nav-link" @click="getSubscription()">订阅列表</a>
        </div>
        <div v-else class="card-header" align="center">
            <form class="form" @submit.prevent>
                <div class="form-group">
                    <input class="form-control" name="username" type="text" placeholder="用户名" v-model="username"
                           required pattern="\w{3,12}" />
                           <p class="text-muted"><small>3~12位字母、数字、下划线</small></p>
                </div>
                <div class="form-group">
                    <input class="form-control" name= "password" type="password" placeholder="密码" v-model="password"
                           required pattern="\w{4,}"/>
                           <p class="text-muted"><small>至少4位，字母数字下划线</small></p>
                </div>
                <div class="form-group clearfix">
                    <input type="submit" @click="register()" class="btn btn-outline-danger float-xs-left" 
                    	value="注册" :disabled="!validation" />
                    <input type="submit" @click="login()" class="btn btn-outline-success float-xs-right" 
                    	value="登录" :disabled="!validation" />
                </div>
            </form>
        </div>
        <div class="card-block">
            <p v-for="(mp, idx) in subscribeList" @mouseover="showRemove(idx)" @mouseout="hideRemove(idx)">
                <small>
                    <a class="nav-link" :href="mp.encGzhUrl" target="_blank">
                        <img :src="mp.image" class="mpavatar img-circle img-responsive" /> {{ mp.mpName }} </a>
                    <a href="javascript:" @click="unsubscribeMp(mp.weixinhao)">
                        <i class="fa fa-lg float-xs-right text-danger sidebar-remove"
                           :class="{'fa-minus-circle': mp.showRemoveBtn}"></i></a></small>

            </p>
        </div>
    </div>
</template>

<script>
    export default {
        name : 'Sidebar',
        data() {
            return {
                is_login: false,
                username: '',
                password: '',
                token: ''
            }
        },
        created: function () {
            // 从LocalStorage中取出数据
            if (window.localStorage.getItem("user")) {
                var userData = JSON.parse(window.localStorage.getItem("user")) ;
                this.token = userData.token;
                this.username = userData.username;
                this.is_login = true
            }
            return this.$store.dispatch('initFromLS', 'init from LS');
        },
        computed : {
            subscribeList () {
                // 从store中取出数据
                return this.$store.state.subscribeList
            },
            validation() {
                var patt1 = /(\w{3,12})/;
                var patt2 = /(\w{4,})/;
//            	alert(this.username + patt1.test(this.username));
                return patt1.test(this.username) && patt2.test(this.password)
            }
        },
        methods : {
            unsubscribeMp(weixinhao) {
                // 删除该公众号
                return this.$store.dispatch('unsubscribeMp',weixinhao);
            },
            showRemove(idx) {
                return this.subscribeList[idx]['showRemoveBtn']= true;
            },
            hideRemove(idx) {
                return this.subscribeList[idx]['showRemoveBtn']= false;
            },
            login() {
//            this.$http.options.headers={
                //'Content-Type':'application/json; charset=UTF-8'
//};
                if (!this.validation) return;
                this.$http.post('/auth',
                	//body
                        {	username: this.username,
                            password: this.password
                        },
                        //options
                        {
                            headers: {'Content-Type':'application/json; charset=UTF-8'}
                        }                 ).then((response) => {
                    // 响应成功回调
                    var data = response.body;
                this.token = data.access_token;
                this.is_login = true;
   //             alert(data.access_token);
                var userData = {'username': this.username, 'token': this.token};
                window.localStorage.setItem("user", JSON.stringify(userData))

            }, (response) => {
                    // 响应错误回调
                    alert('登录出错了！ '+ response.status+ response.statusText)
                });
            },
            register() {
                if (!this.validation) return;
                this.$http.post('/api/v1.0/register',
//body
                        {	username: this.username,
                            password: this.password
                        },
                        //options
                        {
                            //             emulateHTTP: true,
                            headers: {'Content-Type':'application/json; charset=UTF-8'}
                        }                 ).then((response) => {
                    // 响应成功回调
                    var data = response.body;
                if (data.status=='success') {
                    alert('Success! ' + data.msg)
                }
                else {
                    alert(data.msg)
                }
//    this.username = '';
                this.password = ''
            }, (response) => {
                    // 响应错误回调
                    alert('注册出错了！ '+ response.status+ response.statusText)
                });
            },
            logout() {
                this.is_login = false;
                this.password = '';
                this.token = '';
                window.localStorage.removeItem("user")
            },
            getSubscription() {
                this.$http.get('/api/v1.0/mps',
				{	params: { username: this.username }, 
                        	headers: { 'Content-Type': 'application/json; charset=UTF-8',
                        				'Authorization': 'JWT '+this.token }
                        }                 ).then((response) => {
                    // 响应成功回调
                    var data = response.body, mp;
                    // [{"articles_count":2,"image":null,"summary":null,"weixinhao":"aaa"},{"articles_count":0,"image":null,"summary":null,"weixinhao":"bbb"}]
                    for (let mp of data) {
                    	alert(mp.weixinhao)
                    }
            }, (response) => {
                    // 响应错误回调
                    alert('同步出错了！ '+ JSON.stringify(response))
                    if (response.status == 401) {
                    	alert('登录超时，请重新登录');
                    	this.is_login = false;
                    	this.password = ''
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