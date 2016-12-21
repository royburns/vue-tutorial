<template>
    <div class="card">
        <div v-if="is_login" class="card-header" align="center">
            <img src="http://avatar.csdn.net/1/E/E/1_kevin_qq.jpg"
                 class="avatar img-circle img-responsive" />
            <p><strong> 非梦</strong></p>
            <p class="card-title">订阅列表</p>
        </div>
         <div v-else class="card-header" align="center">
        <form class="form">
          <input class="form-control" name="username" type="text" placeholder="用户名" v-model="username">
          <input class="form-control" name= "password" type="password" placeholder="密码" v-model="password">
          <a href="javascript:" @click="login()">登录</a>
          <router-link to="/search"><i class="fa fa-search btn btn-outline-success" @click=""></i></router-link>
          <i class="fa fa-user-o btn btn-outline-success"></i>
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
            password: ''
            }
        },
        created: function () {
            // 从LocalStorage中取出数据
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
            this.$http.options.headers={
	'Content-Type':'application/json; charset=UTF-8'
};
                  this.$http.post("http://localhost:5000/auth",
                    {	username: this.username,
			password: this.password
                    }).then(function(res){
                    alert(JSON.parse(res.bodyText) );
                },function(){
                    this.isSearching = false;
                    alert('Sorry, 网络似乎有问题')
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