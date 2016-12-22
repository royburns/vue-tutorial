<template>
    <div class="card">
        <div v-if="is_login" class="card-header" align="center">
            <img src="http://avatar.csdn.net/1/E/E/1_kevin_qq.jpg"
                 class="avatar img-circle img-responsive" />
            <p><strong v-text="username"></strong>
            <a href="javascript:" @click="logout()" title="退出">
                        <i class="fa fa-sign-out float-xs-right"></i></a>
            </p>
            <p class="card-title">订阅列表</p>
        </div>
         <div v-else class="card-header" align="center">
        <form class="form" @submit.prevent>
        <div class="form-group">
          <input class="form-control" name="username" type="text" placeholder="用户名(3~12字符)" v-model="username" 
                required pattern="\w{3,12}" />
          </div>
          <div class="form-group">
          <input class="form-control" name= "password" type="password" placeholder="密码(至少4位)" v-model="password" 
                required pattern="\w{4,}"/>
          </div>
          <div class="form-group">
          <input type="submit" @click="register()" class="btn btn-outline-danger" value="注册"/>
          <input type="submit" @click="login()" class="btn btn-outline-success" value="登录"/>
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
            token: '',
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
    alert(data.access_token);
    var userData = {'username': this.username, 'token': this.token};
    window.localStorage.setItem("user", JSON.stringify(userData))

}, (response) => {
    // 响应错误回调
    alert('登录出错了！ '+ response.status+ response.statusText)
});
            },
            register() {
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
    this.username = '';
    this.password = ''
}, (response) => {
    // 响应错误回调
    alert('注册出错了！ '+ response.status+ response.statusText)
});
            },
            logout() {
    this.is_login = false;
    this.token = '';
    window.localStorage.removeItem("user")
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