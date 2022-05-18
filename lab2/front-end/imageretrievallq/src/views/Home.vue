<template>
  <div class="home">
    <!--搜索顶栏-->
    <a-row>
      <a-col :span="8">
        <a-carousel autoplay style="width: 60%;margin-left: 10%" :dots ="false">
          <img src="https://joes-bucket.oss-cn-shanghai.aliyuncs.com/img/flame-design-science.gif" alt=""/>
          <img src="https://joes-bucket.oss-cn-shanghai.aliyuncs.com/img/puzzle-search.gif" alt=""/>
          <img src="https://joes-bucket.oss-cn-shanghai.aliyuncs.com/img/puzzle-39.gif"/>
          <img src="https://joes-bucket.oss-cn-shanghai.aliyuncs.com/img/puzzle-18.gif"/>
        </a-carousel>
      </a-col>
      <a-col :span="16">
        <a-row>
          <!--          <h1 contenteditable spellcheck="false">Search & Explore!</h1>-->
          <div class="container">
            <div class="neon">Image Retrieval&nbsp</div>
            <div class="flux">Search!</div>
          </div>
        </a-row>
        <a-row >
          <a-col :span="8">
            <el-upload
                style="margin-left: 0"
                class="upload-demo"
                ref="upload"
                action="http://100.80.144.51:5000/imgUpload"
                list-type="picture-card"
                :file-list="fileList"
                :limit="1"
                :auto-upload="false"
                :on-exceed="showUploadExceedMessage"
                :on-success="showResult"
                :on-change="handleChange"
                :on-remove="handleRemove"
            >
              <el-button
                  slot="trigger"
                  size="small"
                  circle
                  icon="el-icon-plus"
                  style="border-width: 0"
                  :autofocus="true"></el-button>

              <div slot="file" slot-scope="{file}" style="width: 100%;height: 100%">
                <el-image style="width: 100%;height: 100%"
                        :src="file.url" alt="" fit="cover"></el-image>
                <span class="el-upload-list__item-actions">
                  <span class="el-upload-list__item-preview" @click="handlePictureCardPreview(file)">
                    <i class="el-icon-zoom-in"></i>
                  </span>
                  <span
                      v-if="!disabled"
                      class="el-upload-list__item-delete"
                      @click="handleRemove(file)">
                      <i class="el-icon-delete"></i>
                  </span>
                </span>
              </div>
              <div id="testbutton1"
                   v-if="!hasSearchResult"
                    @click="search"
                    style="margin-top: 5%">
              </div>

            </el-upload>
          <el-dialog :visible.sync="dialogVisible">
            <img width="100%" :src="dialogImageUrl" alt="">
          </el-dialog>

          </a-col>
          <a-col :span="4">
            <a-row>
              <div v-show="!favoriteListTag"
                   id="testbutton2"
                   style="margin-top: 10%"
                   @click="goTofavoriteList"
              >
              </div>
              <div v-show="favoriteListTag"
                   id="testbutton3"
                   style="margin-top: 10%"
                   @click="()=>favoriteListTag = false"
              >
              </div>
            </a-row>
            <a-row>
                <div
                    class="flux"
                    style="font-size: 0.7rem;font-family: Avenir;font-weight: bold;height:70px"
                    v-if="!favoriteListTag"
                      >
                  <i>Choose result number:{{chosedResultNum}}</i>
                </div>
            </a-row>
            <a-row>
              <a-slider
                  v-show="!favoriteListTag"
                  :min="0"
                  :max="maxResultNum"
                  :value="chosedResultNum"
                  @change="handleNumChange" />
            </a-row>
          </a-col>
          <!--条件筛选-->
          <a-col :span="6">
            <a-select
                v-if="hasSearchResult && !favoriteListTag"
                show-search
                mode="multiple"
                :default-value="[]"
                @change="addChosedList"
                style="width: 80%;margin-top: 10%"
              placeholder="filter the tags!">
                <a-select-option v-for="(item,index) in tagArray" :key="index" :value="item">
                  {{item}}
                </a-select-option>
            </a-select>
          </a-col>
          <!--筛选-->
          <a-col :span="6">
            <a-row>
              <div id="testbutton"
                   v-if="hasSearchResult && !favoriteListTag"
                  style="margin-top: 10%"
                  @click="filterResult">
              </div>
            </a-row>

          </a-col>
        </a-row>
      </a-col>
    </a-row>
    <!--加载框-->
    <div class="card-container" v-if="isLoading">
      <div class="flux" style="margin-left:40%;">Loading!</div>
      <div >
        <ul class="loading-container" style="margin-top: -20%">
          <li class="li1"></li>
          <li class="li2"></li>
          <li class="li3"></li>
          <li class="li4"></li>
          <li class="li5"></li>
          <li class="li6"></li>
          <li class="li7"></li>
        </ul>
      </div>
    </div>
    <div class="card-container" v-if="!this.favoriteListTag && this.filteredResultList.length === 0 && !isLoading">
      <div
          class="flux" style="font-size:2rem;width:100%;height:50px;font-family: Emoji">
        <i>Upload your image and explore ！😊</i>
      </div>
    </div>
    <!--图片搜索结果-->
    <div
        class="neon" style="font-size:2rem;margin-left: 5%;width:40%;height:50px;font-family: Bahnschrift"
        v-if="!isLoading && !this.favoriteListTag && this.filteredResultList.length > 0">
      Found {{this.resultNum}} results:
    </div>
    <div class="card-container" v-if="!isLoading && !this.favoriteListTag">
      <div  v-for="(item,index) in filteredResultList.slice(0,resultNum)"
            :key=index
            class="image-card"
            style="position: relative">
        <el-image
            :lazy = "false"
            fit="cover"
            style="width: 100%; height: 100%;border-radius: 20px"
            :src="require('../../database/dataset/'+item.imgName)"
            :preview-src-list="[require('../../database/dataset/'+item.imgName)]">
        </el-image>
        <h1 style="position: absolute;cursor:pointer;top:5%;left: 10%;font-family: neon;color: white;font-weight: bold"
            class="tag" >
          {{item.imgName.slice(0,item.imgName.indexOf('.'))}}
        </h1>
        <!--每张照片的标签-->
        <div style="width: 40%;height: 10%;cursor:pointer;background-color: rgba(28,28,28,0.55);position: absolute;top:80%;left:5%;border-radius: 10px"
              class="tag" >
          <p style="color: white;font-family: neon;font-weight: bold">
            {{item.tag}}
          </p>
        </div>
        <!--收藏按钮-->
        <svg v-if="!item.liked" t="1652809329728"
             style="position: absolute;top:5%;left:80%"

             @click="addFavoriteList(index)"
             cursor='pointer'
             class="icon-favorite"
             viewBox="0 0 1158 1024"
             version="1.1"
             xmlns="http://www.w3.org/2000/svg" p-id="2151" width="30" height="30">
          <path d="M633.712038 838.465517c6.397741 0 6.397741 0 6.397741-6.397741 25.590963-19.193222 51.181926-38.386445 63.977408-51.181926 19.193222-12.795482 76.77289-63.977408 89.568371-76.77289 31.988704-25.590963 57.579667-51.181926 76.77289-70.375149C979.190041 531.373959 1023.974227 448.203328 1030.371968 333.043994c12.795482-236.71641-249.511891-326.284781-403.057671-134.352557l-12.795481 12.795482c-6.397741 6.397741-6.397741 12.795482-12.795482 12.795481l-38.386445 38.386445-38.386444-38.386445-12.795482-12.795481c-6.397741-6.397741-6.397741-12.795482-12.795482-12.795482-147.148038-185.534483-409.455411-95.966112-403.05767 127.954816 6.397741 121.557075 57.579667 211.125446 172.739002 319.88704 19.193222 19.193222 44.784186 38.386445 70.375148 63.977408 6.397741 6.397741 63.977408 51.181926 76.77289 63.977408 12.795482 12.795482 31.988704 25.590963 57.579667 44.784185 6.397741 0 6.397741 6.397741 12.795482 12.795482 19.193222 12.795482 44.784186 31.988704 63.977408 44.784186 44.784186-6.397741 63.977408-25.590963 83.17063-38.386445z m499.023782-492.626042c-6.397741 147.148038-70.375149 249.511891-191.932224 371.068967-25.590963 19.193222-44.784186 44.784186-83.17063 70.375148-12.795482 12.795482-70.375149 57.579667-89.568371 76.77289-12.795482 12.795482-38.386445 31.988704-63.977408 51.181926-6.397741 0-6.397741 0-6.397741 6.397741-19.193222 12.795482-38.386445 31.988704-63.977408 44.784186-12.795482 6.397741-25.590963 19.193222-25.590963 19.193222l-25.590963 19.193223-31.988704-19.193223c-6.397741-6.397741-19.193222-12.795482-31.988704-19.193222-25.590963-12.795482-44.784186-31.988704-70.375149-44.784186-6.397741-6.397741-12.795482-6.397741-12.795482-12.795481-25.590963-19.193222-51.181926-38.386445-70.375148-51.181927-19.193222-12.795482-70.375149-63.977408-76.77289-63.977408-31.988704-25.590963-51.181926-44.784186-76.772889-63.977408C70.710848 601.749107 6.73344 492.987514 0.335699 339.441735c-12.795482-319.88704 345.478003-454.239597 563.00119-223.920928 223.920928-230.318669 582.194413-95.966112 569.398931 230.318668z" fill="#e6e6e6" p-id="2152">

          </path>
        </svg>
        <!--点击取消收藏-->
        <svg
            v-if="item.liked"
            @click="cancelLiked(index)"
            style="position: absolute;top:5%;left:80%"
            t="1652881829628"
            class="icon-favorite"
            cursor="pointer"
            viewBox="0 0 1024 1024"
            version="1.1"
            xmlns="http://www.w3.org/2000/svg"
            p-id="3100"
            width="30"
            height="30">
          <path d="M913.92 208.384c-98.816-98.816-258.56-98.816-357.376 0l-41.984 41.984-41.984-41.984c-98.816-98.816-258.56-98.816-357.376 0-98.304 98.816-98.304 258.56 0.512 357.376l52.224 52.224 337.408 337.408c5.632 5.632 14.336 5.632 19.968 0l337.408-337.408 52.224-52.224c97.792-98.816 97.792-258.56-1.024-357.376z" fill="#FC053B" p-id="3101">

          </path>
        </svg>

      </div>
    </div>
    <!--收藏夹页面-->
    <div class="card-container" v-if="this.favoriteListTag && this.favoriteResultList.length > 0">
      <div  v-for="(item,index) in favoriteResultList"
            :key=index
            class="image-card"
            style="position: relative">
        <el-image
            :lazy = "true"
            fit="cover"
            style="width: 100%; height: 100%;border-radius: 20px"
            :src="require('../../database/dataset/'+item.imgName)"
            :preview-src-list="[require('../../database/dataset/'+item.imgName)]">
        </el-image>
        <h1 style="position: absolute;cursor:pointer;top:5%;left: 10%;font-family: neon;color: white;font-weight: bold"
            class="tag" >
          {{item.imgName.slice(0,item.imgName.indexOf('.'))}}
        </h1>
        <!--每张照片的标签-->
        <div style="width: 40%;height: 10%;cursor:pointer;background-color: rgba(28,28,28,0.55);position: absolute;top:80%;left:5%;border-radius: 10px"
             class="tag" >
          <p style="color: white;font-family: neon;font-weight: bold">
            {{item.tag}}
          </p>
        </div>
        <!--收藏按钮-->
        <svg v-if="!item.liked" t="1652809329728"
             style="position: absolute;top:5%;left:80%"

             @click="addFavoriteList(index)"
             cursor='pointer'
             class="icon-favorite"
             viewBox="0 0 1158 1024"
             version="1.1"
             xmlns="http://www.w3.org/2000/svg" p-id="2151" width="30" height="30">
          <path d="M633.712038 838.465517c6.397741 0 6.397741 0 6.397741-6.397741 25.590963-19.193222 51.181926-38.386445 63.977408-51.181926 19.193222-12.795482 76.77289-63.977408 89.568371-76.77289 31.988704-25.590963 57.579667-51.181926 76.77289-70.375149C979.190041 531.373959 1023.974227 448.203328 1030.371968 333.043994c12.795482-236.71641-249.511891-326.284781-403.057671-134.352557l-12.795481 12.795482c-6.397741 6.397741-6.397741 12.795482-12.795482 12.795481l-38.386445 38.386445-38.386444-38.386445-12.795482-12.795481c-6.397741-6.397741-6.397741-12.795482-12.795482-12.795482-147.148038-185.534483-409.455411-95.966112-403.05767 127.954816 6.397741 121.557075 57.579667 211.125446 172.739002 319.88704 19.193222 19.193222 44.784186 38.386445 70.375148 63.977408 6.397741 6.397741 63.977408 51.181926 76.77289 63.977408 12.795482 12.795482 31.988704 25.590963 57.579667 44.784185 6.397741 0 6.397741 6.397741 12.795482 12.795482 19.193222 12.795482 44.784186 31.988704 63.977408 44.784186 44.784186-6.397741 63.977408-25.590963 83.17063-38.386445z m499.023782-492.626042c-6.397741 147.148038-70.375149 249.511891-191.932224 371.068967-25.590963 19.193222-44.784186 44.784186-83.17063 70.375148-12.795482 12.795482-70.375149 57.579667-89.568371 76.77289-12.795482 12.795482-38.386445 31.988704-63.977408 51.181926-6.397741 0-6.397741 0-6.397741 6.397741-19.193222 12.795482-38.386445 31.988704-63.977408 44.784186-12.795482 6.397741-25.590963 19.193222-25.590963 19.193222l-25.590963 19.193223-31.988704-19.193223c-6.397741-6.397741-19.193222-12.795482-31.988704-19.193222-25.590963-12.795482-44.784186-31.988704-70.375149-44.784186-6.397741-6.397741-12.795482-6.397741-12.795482-12.795481-25.590963-19.193222-51.181926-38.386445-70.375148-51.181927-19.193222-12.795482-70.375149-63.977408-76.77289-63.977408-31.988704-25.590963-51.181926-44.784186-76.772889-63.977408C70.710848 601.749107 6.73344 492.987514 0.335699 339.441735c-12.795482-319.88704 345.478003-454.239597 563.00119-223.920928 223.920928-230.318669 582.194413-95.966112 569.398931 230.318668z" fill="#e6e6e6" p-id="2152">

          </path>
        </svg>
        <!--点击取消收藏-->
        <svg
            v-if="item.liked"
            @click="cancelLiked(index)"
            style="position: absolute;top:5%;left:80%"
            t="1652881829628"
            class="icon-favorite"
            cursor="pointer"
            viewBox="0 0 1024 1024"
            version="1.1"
            xmlns="http://www.w3.org/2000/svg"
            p-id="3100"
            width="30"
            height="30">
          <path d="M913.92 208.384c-98.816-98.816-258.56-98.816-357.376 0l-41.984 41.984-41.984-41.984c-98.816-98.816-258.56-98.816-357.376 0-98.304 98.816-98.304 258.56 0.512 357.376l52.224 52.224 337.408 337.408c5.632 5.632 14.336 5.632 19.968 0l337.408-337.408 52.224-52.224c97.792-98.816 97.792-258.56-1.024-357.376z" fill="#FC053B" p-id="3101">
          </path>
        </svg>

      </div>
    </div>

    <div class="card-container" v-if="this.favoriteListTag && this.favoriteResultList.length === 0">
      <div
          class="neon" style="font-size:2rem;width:100%;height:50px;font-family: Bahnschrift">
        You have not add any image to your favorite list.
      </div>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import $ from 'jquery/dist/jquery'
const tagArray = [
  "plant_life",
  "animals",
  "people",
  "tree",
  "bird",
  "water",
  "sky",
  "dog",
  "indoor",
  "transport",
  "sunset",
  "structures",
  "food",
  "portrait",
  "night",
  "male"
]

export default {
  name: 'Home',
  components: {},
  data() {
    return {
      previewVisible: false,
      previewImage: '',
      fileList: [],
      //是否开始上搜索
      isSearch: false,
      loading: false,
      //是否在进行搜索加载
      isLoading: false,
      //图片选择表单
      imageForm: this.$form.createForm(this, {name: 'imageForm'}),
      //获取的图片url
      imageurlList: [
        "https://joes-bucket.oss-cn-shanghai.aliyuncs.com/img/%E8%AF%81%E4%BB%B6%E7%85%A7.jpg"
      ],
      fileData: null,
      dialogImageUrl: '',
      dialogVisible: false,
      disabled: false,
      //结果的图片名称
      imageNameList: [],
      //结果的标签名称
      tagList: [],
      //筛选的标签名称
      chosedTagList: [],
      //已有的标签名称
      tagArray,
      //是否有搜索结果
      hasSearchResult: false,
      //搜索的结果数量
      maxResultNum: 100,
      //选择的要搜索的结果数量
      chosedResultNum: 50,
      //获取到的图片对象数组
      picResultList: [],
      resultNum: 0,
      //筛选的列表
      filteredResultList: [],
      //是否跳转到收藏板块
      favoriteListTag: false,
      //收藏夹列表数组
      favoriteResultList: [],
      //上传的文件是否合法
      isLegal : true
  }
  },
  methods: {
    //进行图片搜索
    search() {
      if (this.fileList.length !== 0) {
        if(!this.isLegal){
          this.$notify({
            title: 'Oops!',
            message: 'The format of the file you uploaded does not meet the requirements! Please delete and re-upload!',
            type: 'warning',
            duration: 5000
          });
          return ;
        }
        this.isLoading = true;
        this.$refs.upload.submit();
      } else {
        this.$notify({
          title: 'Oops!',
          message: 'Please upload at least one picture!',
          type: 'warning',
          duration: 5000
        });
      }
    },
    handleChange(file) {
      this.fileList.push(file)
      let legalSet = new Set(['png','jpg','jpeg'])
      if(!legalSet.has(file.name.split('.')[1])) {
        this.isLegal = false
      }
    },
    //返回搜索结果
    showResult(res) {
      this.hasSearchResult = true
      this.isLoading = false
      let nameArr = res.map(item => {
        return item.split('\\')[1]
      })
      let _this = this
      let likeList = []
      if (localStorage.getItem('favorite') !== '' && localStorage.getItem('favorite')) {
        likeList = JSON.parse(localStorage.getItem('favorite'))
      }
      let likeSet = new Set();
      likeList.forEach((item) => {
        likeSet.add(item.imgName);
      })
      console.log(likeSet)
      this.$axios.get('/tagdict.json').then(res => {
        nameArr.forEach((item) => {
          let liked = false;
          if (likeSet.has(item))
            liked = true;
          _this.picResultList.push({
            imgName: item,
            tag: res.data[item],
            liked: liked
          })
          _this.filteredResultList.push({
            imgName: item,
            tag: res.data[item],
            liked: liked
          })
        })
      })
      this.fileList.shift();
      //按照数量进行裁剪
      this.resultNum = this.chosedResultNum

    },
    handleRemove(file) {
      this.hasSearchResult = false
      this.maxResultNum = 100;
      this.fileList = []
    },
    handlePictureCardPreview(file) {
      this.dialogImageUrl = file.url;
      this.dialogVisible = true;
    },
    showUploadExceedMessage() {
      this.$notify({
        title: 'Oops!',
        message: 'Allow only one image to be searched！',
        type: 'warning',
        duration: 5000
      });
    },
    //收藏图片
    addFavoriteList(index) {
      if (localStorage.getItem('favorite') == '' || !localStorage.getItem('favorite')) {
        localStorage.setItem('favorite', JSON.stringify([]));
      }
      let obj = {
        imgName: this.filteredResultList[index].imgName,
        tag: this.filteredResultList[index].tag,
        liked: true
      };
      let arr = JSON.parse(localStorage.getItem('favorite'));
      arr.push(obj)
      localStorage.setItem('favorite', JSON.stringify(arr));
      this.filteredResultList[index].liked = true
      this.$notify({
        title: '!!!',
        message: 'You have add ' + obj.imgName + " to your favorite list",
        type: 'success',
        duration: 5000
      });
    },
    //取消收藏
    cancelLiked(index) {
      if(this.favoriteListTag)
        this.favoriteResultList[index].liked = false
      else
        this.filteredResultList[index].liked = false
      let str = this.favoriteListTag ? this.favoriteResultList[index].imgName : this.filteredResultList[index].imgName
      this.$notify({
        title: '!!!',
        message: 'You have removed ' + str  + " from your favorite list",
        type: 'success',
        duration: 5000
      });
      let arr = JSON.parse(localStorage.getItem('favorite'));
      for (let i = 0; i < arr.length; i++) {
        if (this.favoriteListTag ? this.favoriteResultList[index].imgName : this.filteredResultList[index].imgName === arr[i].imgName) {
          arr.splice(i, 1);
          localStorage.setItem('favorite', JSON.stringify(arr));
        }
      }
    },
  //添加选中的标签
  addChosedList(value) {
    this.chosedTagList = value;
    if (this.chosedTagList.length !== 0) {
      this.maxResultNum = this.picResultList.reduce((result, item) => {
        if (this.chosedTagList.indexOf(item.tag) !== -1) {
          result++;
        }
        return result;
      }, 0)
    }
  },
  //根据标签筛选结果
  filterResult() {

    if (this.chosedTagList.length !== 0) {
      this.filteredResultList = []
      this.picResultList.forEach((item, index) => {
        if (this.chosedTagList.indexOf(item.tag) !== -1) {
          this.filteredResultList.push({
            imgName: item.imgName,
            tag: item.tag,
            liked: false
          })
        }
      })
    }
    this.resultNum = this.chosedResultNum
  },

  //搜索结果的数量改变
  handleNumChange(value) {
    this.chosedResultNum = value
  },
  //跳转到收藏页面
  goTofavoriteList() {
    this.favoriteListTag = true;
    if (localStorage.getItem('favorite') !== '' && localStorage.getItem('favorite')) {
      this.favoriteResultList = JSON.parse(localStorage.getItem('favorite'))
    }
  }

  },
  created() {

  }
}
</script>
<style>
.upload-demo /deep/ .el-upload--picture-card .upload_btn{
  background: #fff;
  color: #3C56C6;
  border: none;
  border-radius: 0;
  position: absolute;
  bottom: -5px;
  right: -90px;
  pointer-events: auto;
text-decoration: underline;
}
.upload-demo /deep/ .el-upload--picture-card,
.upload-demo /deep/ .el-upload-list--picture-card .el-upload-list__item{
  line-height: 100px;
  font-size: 12px;
  height: 100px;
  width: 100px;
  position: relative;
  background: #F8F8F8;
  border: 1px solid #d2d2d2;
  border-radius: 0;
}
.upload-demo /deep/ .el-upload--picture-card{
  pointer-events: none;
}

html,
body {
  background-color: black !important;
}

.card-container{
  width: 80%;
  height: 100vh;
  position: absolute;
  margin: auto;
  left:0;
  right:0;
  display: flex;
  justify-content: flex-start;
  flex-wrap: wrap;
  align-items: stretch;
  align-content: flex-start;
}

.image-card{
  margin-left: 4%;
  margin-top: 4%;
  background-color: white;
  width: 250px;
  height: 250px;
  border-radius: 20px;
  box-shadow: rgba(50, 50, 93, 0.25) 0px 50px 100px -20px, rgba(0, 0, 0, 0.3) 0px 30px 60px -30px, rgba(10, 37, 64, 0.35) 0px -2px 6px 0px inset;
  -webkit-transition-duration: 0.3s;
  transition-duration: 0.3s;
  -webkit-transition-property: transform;
  transition-property:  transform;
}

.image-card:hover,.image-card:focus,.image-card:active{
  position: relative;

  -webkit-transform: scale(1.1);
  transform: scale(1.1);
}

.icon-favorite,.tag{
  -webkit-transition-duration: 0.3s;
  transition-duration: 0.3s;
  -webkit-transition-property: transform;
  transition-property:  transform;
}
.icon-favorite:hover,.tag:hover{
  position: relative;

  -webkit-transform: scale(1.1);
  transform: scale(1.5);
}


.home{
  position: relative;
}

.loading-container{
  position:absolute;
  top:50%;
  left:50%;
  transform:translate(-50%,-50%);
  margin:0;
  padding:0;
  display:flex;
}

@keyframes grow
{
  0% , 40% , 100%
  {
    transform:scale(0.2);
  }
  20%{
    transform:scale(1);

  }
}

.li1{
  animation-delay:-1.4s;
  background:#ffff00;
  box-shadow:0 0 50px #ffff00;
  list-style:none;
  width:40px;
  height:40px;
  border-radius:50%;
  animation:grow 1.6s ease-in-out infinite;

}
.li2{
  animation-delay:-1.2s;
  background:#76ff03;
  box-shadow:0 0 50px #76ff03;
  list-style:none;
  width:40px;
  height:40px;
  border-radius:50%;
  animation:grow 1.6s ease-in-out infinite;

}
.li3{
  animation-delay:-1s;
  background:#f06292;
  box-shadow:0 0 50px #f06292;
  list-style:none;
  width:40px;
  height:40px;
  border-radius:50%;
  animation:grow 1.6s ease-in-out infinite;

}
.li4{
  animation-delay:-0.8s;
  background:#4fc3f7;
  box-shadow:0 0 50px #4fc3f7;
  list-style:none;
  width:40px;
  height:40px;
  border-radius:50%;
  animation:grow 1.6s ease-in-out infinite;

}
.li5{
  animation-delay:-0.6s;
  background:#ba68c8;
  box-shadow:0 0 50px #ba68c8;
  list-style:none;
  width:40px;
  height:40px;
  border-radius:50%;
  animation:grow 1.6s ease-in-out infinite;

}
.li6{
  animation-delay:-0.4s;
  background:#f57c00;
  box-shadow:0 0 50px #f57c00;
  list-style:none;
  width:40px;
  height:40px;
  background:#fff;
  border-radius:50%;
  animation:grow 1.6s ease-in-out infinite;

}
.li7{
  animation-delay:-0.2s;
  background:#673ab7;
  box-shadow:0 0 50px #673ab7;
  list-style:none;
  width:40px;
  height:40px;
  background:#fff;
  border-radius:50%;
  animation:grow 1.6s ease-in-out infinite;

}




@font-face {
  font-family: neon;
  src: url(https://s3-us-west-2.amazonaws.com/s.cdpn.io/707108/neon.ttf);
}

.container {
  display: inline-flex;
  text-align: center;
  vertical-align: middle;
}

.neon {
  font-family: neon;
  color: #FB4264;
  font-size: 4vw;
  line-height: 9vw;
  text-shadow: 0 0 3vw #F40A35;
}

.flux {
  font-family: neon;
  color: #426DFB;
  font-size: 4vw;
  line-height: 9vw;
  text-shadow: 0 0 3vw #2356FF;
}

.neon {
  animation: neon 1s ease infinite;
  -moz-animation: neon 1s ease infinite;
  -webkit-animation: neon 1s ease infinite;
}

@keyframes neon {
  0%,
  100% {
    text-shadow: 0 0 1vw #FA1C16, 0 0 3vw #FA1C16, 0 0 10vw #FA1C16, 0 0 10vw #FA1C16, 0 0 .4vw #FED128, .5vw .5vw .1vw #806914;
    color: #FED128;
  }
  50% {
    text-shadow: 0 0 .5vw #800E0B, 0 0 1.5vw #800E0B, 0 0 5vw #800E0B, 0 0 5vw #800E0B, 0 0 .2vw #800E0B, .5vw .5vw .1vw #40340A;
    color: #806914;
  }
}

.flux {
  animation: flux 2s linear infinite;
  -moz-animation: flux 2s linear infinite;
  -webkit-animation: flux 2s linear infinite;
  -o-animation: flux 2s linear infinite;
}

@keyframes flux {
  0%,
  100% {
    text-shadow: 0 0 1vw #1041FF, 0 0 3vw #1041FF, 0 0 10vw #1041FF, 0 0 10vw #1041FF, 0 0 .4vw #8BFDFE, .5vw .5vw .1vw #147280;
    color: #28D7FE;
  }
  50% {
    text-shadow: 0 0 .5vw #082180, 0 0 1.5vw #082180, 0 0 5vw #082180, 0 0 5vw #082180, 0 0 .2vw #082180, .5vw .5vw .1vw #0A3940;
    color: #146C80;
  }
}


/*glow*/

@keyframes neon1 {
  from {
    text-shadow: 0 0 10px #fff, 0 0 20px #fff, 0 0 30px #fff, 0 0 40px #ff00de,
    0 0 70px #ff00de, 0 0 80px #ff00de, 0 0 100px #ff00de, 0 0 150px #ff00de;
  }
  to {
    text-shadow: 0 0 5px #fff, 0 0 10px #fff, 0 0 15px #fff, 0 0 20px #ff00de,
    0 0 35px #ff00de, 0 0 40px #ff00de, 0 0 50px #ff00de, 0 0 75px #ff00de;
  }
}


.my-font{
  text-align: center;
  font-size: 7em;
  margin-bottom: 0;
  margin-top: 0;
  line-height: 1;
  text-decoration: none;
  color: #fff;
  font-family: Lato, "Trebuchet MS", "Verdana", "sans-serif";
  animation: neon1 1.5s ease-in-out infinite alternate;
}

#testbutton,#testbutton1,#testbutton2 , #testbutton3{
  width: 150px;
  height:50px;
  font-family: Lato, "Trebuchet MS", "Verdana", "sans-serif";
  border-radius:180px;
  position:relative;
  left:calc(50% - 75px);
  top:calc(50% - 25px);
  background: linear-gradient(60deg, #f79533, #f37055, #ef4e7b, #a166ab, #5073b8, #1098ad, #07b39b, #6fba82);
  cursor:pointer;
  line-height:12px;
  -webkit-transition-duration: 0.3s;
  transition-duration: 0.3s;
  -webkit-transition-property: transform;
  transition-property:  transform;
}

#testbutton:hover,#testbutton1:hover,#testbutton2:hover, #testbutton3:hover{
  position: relative;

  -webkit-transform: scale(1.1);
  transform: scale(1.1);
}
#testbutton:before ,#testbutton1:before,#testbutton2:before, #testbutton3:before{
  content:'';
  z-index:1;
  position:absolute;
  display:block;
  width:80%;
  height:70%;
  top:15%;
  left:10%;
  transition: 0.3s opacity ease-in-out;
  filter:blur(15px);
  opacity:0;
  background: linear-gradient(60deg, #f79533, #f37055, #ef4e7b, #a166ab, #5073b8, #1098ad, #07b39b, #6fba82);
}

#testbutton:hover:before ,#testbutton1:hover:before,#testbutton2:hover:before, #testbutton3:hover:before{
  opacity:1;
  transition: 0.3s opacity ease-in-out;
  filter:blur(25px);
  background: linear-gradient(60deg, #f79533, #f37055, #ef4e7b, #a166ab, #5073b8, #1098ad, #07b39b, #6fba82);

}

#testbutton:after{
  content:'Filter!';
  text-align:center;
  line-height:40px;
  font-size:18px;
  color:rgba(235,235,235,1);
  font-weight:bold;
  z-index:5;
  position:absolute;
  display:block;
  border-radius:180px;
  width:92%;
  height:80%;
  top:10%;
  left:4%;
  background-color:rgb(19, 20, 22);


}

#testbutton1:after{
  content:'Search!';
  text-align:center;
  line-height:40px;
  font-size:18px;
  color:rgba(235,235,235,1);
  font-weight:bold;
  z-index:5;
  position:absolute;
  display:block;
  border-radius:180px;
  width:92%;
  height:80%;
  top:10%;
  left:4%;
  background-color:rgb(19, 20, 22);


}

#testbutton2:after{
  content:'My Favorite List';
  text-align:center;
  line-height:40px;
  font-size:18px;
  color:rgba(235,235,235,1);
  font-weight:bold;
  z-index:5;
  position:absolute;
  display:block;
  border-radius:180px;
  width:92%;
  height:80%;
  top:10%;
  left:4%;
  background-color:rgb(19, 20, 22);


}

#testbutton3:after{
  content:'Back';
  text-align:center;
  line-height:40px;
  font-size:18px;
  color:rgba(235,235,235,1);
  font-weight:bold;
  z-index:5;
  position:absolute;
  display:block;
  border-radius:180px;
  width:92%;
  height:80%;
  top:10%;
  left:4%;
  background-color:rgb(19, 20, 22);


}




</style>