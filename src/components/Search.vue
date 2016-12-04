<template>
    <div class="card">
        <div class="card-header" align="center">
            <form class="form-inline">
                <input class="form-control form-control-lg wide" v-model="searchKey" type="text" placeholder="搜索公众号/文章">
                <i class="fa fa-search btn btn-lg btn-outline-success" @click="searchMp()"></i>
            </form>
        </div>
        <div class="card-block" v-if="searchData">
            <h5 align="center">共有{{ searchData.totalItems }}条搜索结果，共{{searchData.totalPages}}页</h5>
        </div>
        <div class="card-block" id="searchResult1">
            <div class="media">
                <div class="media-left imgbox">
                    <a class="" href="#">
                        <img class="media-object rounded"
                             src="http://dl.bizhi.sogou.com/images/2014/04/22/587880.jpg">
                    </a></div>
                <div class="media-body">

                    <h4>这个导演的新片，每一部我必二刷</h4>
                    <p class="text-muted" style="margin-bottom: 0px;">
                        11月的时候，鱼叔采访了自己的偶像——蒂姆·波顿。并有机会提前看到了他的新片，然后写了一篇推文。今天电影上映，鱼叔去电影院二刷。这一次，又
                    </p>
                    <p><small class="text-muted s1">
                        <span @click="subscribe()"><i class="fa fa-star-o fa-lg float-xs-right text-danger"></i></span>
                        <i class="fa fa-eye"></i> 2348 </small>
                        <small class="text-muted"> 	独立鱼电影</small>
                        <small class="text-muted s2"> 1小时前</small>
                    </p>
                </div>
            </div>
            <div class="media" id="searchResult2">
                <div class="media-left imgbox">
                    <a class="" href="#">
                        <img class="media-object rounded "
                             src="http://wx.qlogo.cn/mmhead/Q3auHgzwzM6FDWDyWSNm2AFBwFV6SFMXa20hjbFlWOyGYFQqrryIPw/0">
                    </a></div>
                <div class="media-body">

                    <h4>现在的段子，不动脑子根本就看不懂</h4>
                    <p class="text-muted" style="margin-bottom: 0px;">
                        周末，姑妈让我帮忙表照顾5岁的表弟，晚上我给他洗澡的时候，女票打来电话。因为手不方便拿，就开了免提，她问:在做什么呢？我说...
                    </p>
                    <p><small class="text-muted s1">
                        <a href="javascript:" @click="subscribe()">
                            <i class="fa fa-lg float-xs-right text-danger"
                               :class="{'fa-star': isSubscribe, 'fa-star-o': !isSubscribe,}"></i></a>
                        <i class="fa fa-eye"></i> 1181 </small>
                        <small class="text-muted s1">凤凰网</small>
                        <small class="text-muted s2"> 3小时前</small>
                    </p>
                </div>
            </div>
            <div class="media" v-for="(mp,index) in searchData.items">
                {{index}} {{mp}}

                <div class="media-body">
                {{index}}  {{mp}}

                </div>
            </div>
        </div>
    </div>
</template>

<style>
    .form-inline .wide {
        width: 80%;
    }
    .imgbox {
        width: 100px;
        height: 120px;
        overflow: hidden;
    }
    .imgbox img{
        max-width: 100px;
        /*max-height: 120px;*/
    }
    .s1 {
        margin-right: 20px;
    }
    .s2 {
        margin-left: 20px;
    }
</style>

<script>
    export default {
        name : 'SearchResult',
        data() {
            return {
                searchKey: '',
                date : '',
                totalTime : '',
                comment : '',
                mpName: '凤凰网',
                isSubscribe: false,
                myData: '',
                searchData: '',
                searchMpXml: ''
            }
        },
        computed : {
            mpList() {
                // 从store中取出数据
                return this.$store.state.mpList
            }
        },
        methods:{
            searchMp() {
                this.$http.jsonp("http://weixin.sogou.com/weixinwap?_rtype=json&ie=utf8&type=1",
                    {
                        params: {
                            page: 1,
                            type: 1, //公众号
                            query: this.searchKey
                        },
                        jsonp:'cb'
                    }).then(function(res){
                    this.myData = JSON.parse(res.bodyText).totalItems;
                    console.log(this.myData);
                    this.searchData = JSON.parse(res.bodyText);
                    var xmlstr = this.searchData.items;
                    this.searchMpXml = new DOMParser().parseFromString(xmlstr, 'text/xml');
                    this.searchKey = ''
                },function(){
                    console.log(1)
                });
            },
//                axios.jsonp('http://weixin.sogou.com/weixinwap?page=1&_rtype=json&ie=utf8&type=1&query=' + this.searchKey)
//                    .then(function (response) {
//                        console.log(response);
//                        this.searchKey = '';
//                    })
//                    .catch(function (error) {
//                        console.log(error);
//                    });
//                    this.refreshing = true;
//                    this.$nextTick(function () {    //异步更新队列: 可以在数据变化之后立即更新 DOM
//                        this.refreshing = true;
//                        console.log('now is loading:'+this.refreshing) // => 'updated'
//                    });
//                    var self = this;
//                    getJSON('/api/refresh/' + this.table, {
//                    }, function (err, data) {
//                        self.last_update = data.last_update;
//                        self.lz_update = data.lz_update;
//                        self.refreshing = false;   // 隐藏 refreshing
//                        self.msg = data.msg;
//                        this.$nextTick(function () { });
//
//                    });


            subscribe() {
                const mp = {
                    mpName : this.mpName,
                    image : 'https://sfault-avatar.b0.upaiyun.com/888/223/888223038-5646dbc28d530_huge256',
                    date : this.date,
                    totalTime : this.totalTime,
                    comment : this.comment
                };
                for(let item of this.mpList) {
                    if(item.mpName == mp.mpName) return false
                }
                this.$store.dispatch('subscribeMp', mp);
                this.isSubscribe = true;
//                this.$store.dispatch('addTotalTime', this.totalTime);
//                this.$router.go(-1)
            }
        }
    }
</script>
