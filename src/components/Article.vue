<template>
    <div class="card">
        <div class="card-header" align="center">
		<h5 align="center" class="text-muted">公众号[{{ $route.params.mpName || articleList.mpName}}] - 文章列表</h5>
        </div>

        <div class="card-block">
            <div class="media" v-for="(article,index) in articleList.articles">
                <div class="media-left imgbox">
                        <img class="media-object rounded " :src=" 'http://read.html5.qq.com/image?src=forum&q=5&r=0&imgflag=7&imageUrl=' + article.cover" style="margin-top: 5px;">
			</div>
                <div class="media-body">
                    <a :href="article.content_url" target="_blank" class="nav-link"><h5 v-html="article.title"></h5></a>
                    <p class="text-muted" style="margin-bottom: 0px;">
                        <small  title="发表于" class=" s1"> <i class="fa fa-clock-o"></i> {{ formatDate(article.timestamp) }} </small></p>
                    <p class="text-muted" style="margin-bottom: 30px;"> <small class="text-muted s1">
                        <span v-html="article.digest"></span> </small> </p>
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
        height: 140px;
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
                searchInput: '',    // 输入框的值
                searchResultJson: '',
                isSearching: false,
                page: 1,
                hasNextPage: true
            }
        },
        computed : {
            subscribeList() {
                // 从store中取出数据
                return this.$store.state.subscribeList
            },
            mpList() {
                // 从store中取出数据
                return this.$store.state.mpList
            },
            articleList() {
                return JSON.parse(window.localStorage.getItem('weixinhao_'+this.$route.params.id));
            }
          },
        methods:{
        	formatDate(timestamp) {
            	var that = new Date(parseInt(timestamp)*1000), s;
            	 var  y = that.getFullYear(),  
            m = that.getMonth() + 1,  
            d = that.getDate(),  
            hh = that.getHours(),  
            mm = that.getMinutes();  
        s = y + '年';  
        s = s + m + '月' + d + '日 ' + hh + ':' + (mm < 10 ? '0' : '') + mm;  
                return s
            },
             searchMp(pg) {
                this.isSearching = true;
                if (pg==1) {
                    this.searchKey = this.searchInput;
                    this.$store.dispatch('clearSearchResult', 'clear search result');
                    this.page = 1;
                    this.hasNextPage = true
                }
                this.$nextTick(function () { });
                this.$http.jsonp("http://weixin.sogou.com/weixinwap?_rtype=json&ie=utf8",
                    {
                        params: {
                            page: pg,
                            type: 1, //公众号
                            query: this.searchKey
                        },
                        jsonp:'cb'
                    }).then(function(res){
                    this.searchResultJson = JSON.parse(res.bodyText);
                    var mpXmls = this.searchResultJson.items;
                    var i, xmlDoc, mpResult, onePageResults=[];
                    for (i in mpXmls) {
                        mpResult = {};
                        xmlDoc = new DOMParser().parseFromString(mpXmls[i], 'text/xml');
                        mpResult['title'] = xmlDoc.getElementsByTagName("title")[1].childNodes[0].nodeValue;
                        mpResult['name'] = xmlDoc.getElementsByTagName("name")[0].childNodes[0].nodeValue.replace('', '<span class="text-success">').replace('', '</span>');
                        try 	{
                            mpResult['summary'] = xmlDoc.getElementsByTagName("summary")[0].childNodes[0].nodeValue.replace('', '<span class="text-success">').replace('', '</span>')
                        }catch (e) 	{
                            mpResult['summary'] = '无介绍'
                        }

                        mpResult['encGzhUrl'] = xmlDoc.getElementsByTagName("encGzhUrl")[0].childNodes[0].nodeValue; 	// 主页链接
                        try 	{
                            mpResult['url'] = xmlDoc.getElementsByTagName("url")[2].childNodes[0].nodeValue; 		// 最新更新文章
                            mpResult['title1'] = xmlDoc.getElementsByTagName("title1")[0].childNodes[0].nodeValue;
                        }                        catch (e) 	{
                            mpResult['url'] =  '';
                            mpResult['title1'] =  ''
                        }
                        try 	{
                            mpResult['content'] = xmlDoc.getElementsByTagName("content")[0].childNodes[0].nodeValue.replace('', '<span class="text-success">').replace('', '</span>');
                        }                        catch (e) 	{
                            mpResult['content'] = ''
                        }
                        mpResult['date'] = xmlDoc.getElementsByTagName("date")[1].childNodes[0].nodeValue;
                        mpResult['image'] = xmlDoc.getElementsByTagName("image")[0].childNodes[0].nodeValue;
                        mpResult['weixinhao'] = xmlDoc.getElementsByTagName("weixinhao")[0].childNodes[0].nodeValue;
                        var rank = xmlDoc.getElementsByTagName("rank")[0].attributes;
                        mpResult['rank'] = {};
                        mpResult['rank']['fans'] = rank.fans.nodeValue;	// 粉丝数
                        mpResult['rank']['rnum'] = rank.rnum.nodeValue;	// 月发文 篇
                        mpResult['rank']['pnum'] = rank.pnum.nodeValue;	// 平均阅读
                        mpResult['isSubscribed'] = false;
                        for(let item of this.subscribeList) {
                            if(item.weixinhao == mpResult['weixinhao'] ) {
                                mpResult['isSubscribed'] = true;
                                break
                            }
                        }
                        onePageResults.push(mpResult);
                    }
                    this.$store.dispatch('addSearchResultList', onePageResults);
                    this.searchInput = '';
                    this.page = this.page+1;
                    if (this.page > this.searchResultJson.totalPages) {
                        this.hasNextPage = false;
                    }
                    this.isSearching = false;
                },function(){
                    this.isSearching = false;
                    alert('Sorry, 网络似乎有问题')
                });
            },
            subscribe(idx) {
                if (this.mpList[idx].isSubscribed== true ) {
                    // 删除该公众号
                    return this.$store.dispatch('unsubSearchResult',this.mpList[idx].weixinhao);
                }

                var mp = {
                    mpName : this.mpList[idx].title,
                    image : this.mpList[idx].image,
                    date : this.mpList[idx].date,	// 最近更新
                    weixinhao : this.mpList[idx].weixinhao,
                    encGzhUrl : this.mpList[idx].encGzhUrl,
                    subscribeDate : new Date().getTime(),
                    showRemoveBtn: false
                };
                for(let item of this.subscribeList) {
                	// 如果已经订阅，则什么也不做
                    if(item.mpName == mp.mpName) return false
                }
                this.$store.dispatch('subscribeMp', mp);
              //  this.mpList[idx].isSubscribed = true;
            }
        }
    }
</script>
