<template>
    <div class="card">
        <div class="card-header" align="center">
            <img src="http://avatar.csdn.net/1/E/E/1_kevin_qq.jpg"
                 class="avatar img-circle img-responsive" />
            <p><strong> 非梦</strong></p>
            <p class="card-title">1天前 阅读</p>
        </div>
        <div class="card-block">
            <p>
                <img src="http://wx.qlogo.cn/mmhead/Q3auHgzwzM6FDWDyWSNm2AFBwFV6SFMXa20hjbFlWOyGYFQqrryIPw/0"
                     class="mpavatar img-circle img-responsive" />
                <span class="tag tag-danger tag-pill float-xs-right">12</span>
                创意科技生活
            </p>
            <p>
                <img src="http://wx.qlogo.cn/mmhead/Q3auHgzwzM5VP8rbv4fBibDLRoibcezeC7aMx2qs4hfUWtw8Cp6PDZ7Q/0"
                     class="mpavatar img-circle img-responsive" />
                <span class="tag tag-danger tag-pill float-xs-right">3</span>
                科技每日推送
            </p>
            <p v-for="(mp,index) in mpList">
                <img :src="mp.image" class="mpavatar img-circle img-responsive" />
                <span> {{ mp.mpName }} </span>
                <span class="tag tag-danger tag-pill float-xs-right">3</span>
                <a href="javascript:" @click="unsubscribeMp()"><i class="fa fa-trash-o float-xs-right text-danger"></i></a>
            </p>
        </div>
    </div>
</template>

<script>
    export default {
        name : 'Sidebar',
        computed : {
            mpList () {
                // 从store中取出数据
                return this.$store.state.mpList
            }
        },
        methods : {
            unsubscribeMp(idx) {
                // 删除该公众号
                this.$store.dispatch('unsubscribeMp',idx)
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
    .sidebar-new:hover {
        display: none;
    }
    .sidebar-remove {
        display: none;
    }
    .sidebar-remove:hover {
        display: block;
    }

</style>