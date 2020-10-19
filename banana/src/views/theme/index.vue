<template>
  <div>
    <el-tabs
      v-model="activeName"
      type="card"
      @tab-click="handleClick"
      style="margin-left:15px;margin-top:15px;"
    >
      <el-tab-pane label="首页" name="first">
        <el-form ref="shouye_form" :model="shouye_form" label-width="80px">
          <el-form-item label="标题" style="width: 30%">
            <el-input v-model="shouye_data.header_text"></el-input>
          </el-form-item>
          <el-form-item label="背景图" style="width: 30%;">
            <el-upload
              action="http://127.0.0.1:8000/app/img_test/"
              list-type="picture-card"
              :file-list="shouye_data.header_img"
              :on-remove="handleRemove"
              :on-success="header_img"
              name="image"
              limit="1"
            >
              <i class="el-icon-plus"></i>
            </el-upload>
            <el-dialog :visible.sync="dialogVisible">
              <img width="100%" :src="dialogImageUrl" alt />
            </el-dialog>
          </el-form-item>
          <el-form-item label="为您提供">
            <div v-for="(sdfyd,index) in shouye_data.for_you_data" :key="o" class="text item">
              {{ sdfyd.for_you_data_title }}&nbsp;&nbsp;
              <el-dialog
                title
                :visible.sync="sdfyd_dialogFormVisible"
              >
                <el-form ref="sdfyd_form" :model="sdfyd_form" label-width="80px">
                  <el-form-item label="标题">
                    <el-input v-model="sdfyd_form.for_you_data_title"></el-input>
                  </el-form-item>
                  <el-form-item label="描述">
                    <el-input v-model="sdfyd_form.for_you_data_text"></el-input>
                  </el-form-item>
                  <el-form-item label="图片">
                    <el-upload
                      action="http://127.0.0.1:8000/app/img_test/"
                      list-type="picture-card"
                      :on-preview="handlePictureCardPreview"
                      :file-list="sdfyd_form.for_you_data_img"
                      :on-remove="handleRemove"
                      name="image"
                      :on-success="sdfyd_form_img"
                      limit="1"
                    >
                      <i class="el-icon-plus"></i>
                    </el-upload>
                  </el-form-item>
                </el-form>
                <div slot="footer" class="dialog-footer">
                  <el-button @click="sdfyd_dialogFormVisible = false">取 消</el-button>
                  <el-button type="primary" @click="sdfyd_handleClose()">确 定</el-button>
                </div>
              </el-dialog>
              <el-dialog
              title
              :visible.sync="sdfyd_add_dialogFormVisible">
                <el-form ref="sdfyd_form_add" :model="sdfyd_form_add" label-width="80px">
                  <el-form-item label="标题">
                    <el-input v-model="sdfyd_form_add.for_you_data_title"></el-input>
                  </el-form-item>
                  <el-form-item label="描述">
                    <el-input v-model="sdfyd_form_add.for_you_data_text"></el-input>
                  </el-form-item>
                  <el-form-item label="图片">
                    <el-upload
                      action="http://127.0.0.1:8000/app/img_test/"
                      list-type="picture-card"
                      :on-preview="handlePictureCardPreview"
                      :file-list="sdfyd_form_add.for_you_data_img"
                      :on-remove="handleRemove"
                      name="image"
                      :on-success="sdfyd_form_add_img"
                      limit="1"
                    >
                      <i class="el-icon-plus"></i>
                    </el-upload>
                  </el-form-item>
                </el-form>
                <div slot="footer" class="dialog-footer">
                  <el-button @click="sdfyd_dialogFormVisible = false">取 消</el-button>
                  <el-button type="primary" @click="sdfyd_add_handleClose()">确 定</el-button>
                </div>
              </el-dialog>
              <span v-if="shouye_data.for_you_data.length-1===index">
                <el-button
                  type="primary"
                  icon="el-icon-edit"
                  circle
                  size="mini"
                  @click="update_for_you_data(sdfyd,index)"
                ></el-button>
                <el-button
                  type="danger"
                  icon="el-icon-delete"
                  circle
                  size="mini"
                  @click="delete_for_you(sdfyd)"
                ></el-button>
                <el-button type="success" icon="el-icon-plus" circle size="mini" @click="sdfyd_add_dialogFormVisible=true"></el-button>
              </span>
              <span v-else>
                <el-button
                  type="primary"
                  icon="el-icon-edit"
                  circle
                  size="mini"
                  @click="update_for_you_data(sdfyd,index)"
                ></el-button>
                <el-button
                  type="danger"
                  icon="el-icon-delete"
                  circle
                  size="mini"
                  @click="delete_for_you(sdfyd)"
                ></el-button>
              </span>
            </div>
          </el-form-item>
          <el-form-item label="能力展示">
            <div
              v-for="(nlzs,index) in shouye_data.ability_display_data"
              :key="o"
              class="text item"
            >
              {{ nlzs.ability_display_title }}&nbsp;&nbsp;
              <el-dialog
                title
                :visible.sync="nlzs_dialogFormVisible"
              >
                <el-form ref="nlzs_form" :model="nlzs_form" label-width="80px">
                  <el-form-item label="标题">
                    <el-input v-model="nlzs_form.ability_display_title"></el-input>
                  </el-form-item>
                  <el-form-item label="图片">
                    <el-upload
                      action="http://127.0.0.1:8000/app/img_test/"
                      list-type="picture-card"
                      :on-preview="handlePictureCardPreview"
                      :file-list="nlzs_form.ability_display_img"
                      :on-remove="handleRemove"
                      :on-success="nlzs_form_img"
                      name="image"
                      limit="1"
                    >
                      <i class="el-icon-plus"></i>
                    </el-upload>
                  </el-form-item>
                </el-form>
                <div slot="footer" class="dialog-footer">
                  <el-button @click="nlzs_dialogFormVisible = false">取 消</el-button>
                  <el-button type="primary" @click="nlzs_handleClose()">确 定</el-button>
                </div>
              </el-dialog>
              <el-dialog
                title
                :visible.sync="nlzs_add_dialogFormVisible"
              >
                <el-form ref="nlzs_form" :model="nlzs_form" label-width="80px">
                  <el-form-item label="标题">
                    <el-input v-model="nlzs_form_add.ability_display_title"></el-input>
                  </el-form-item>
                  <el-form-item label="图片">
                    <el-upload
                      action="http://127.0.0.1:8000/app/img_test/"
                      list-type="picture-card"
                      :on-preview="handlePictureCardPreview"
                      :file-list="nlzs_form_add.ability_display_img"
                      :on-remove="handleRemove"
                      :on-success="nlzs_form_img_add"
                      name="image"
                      limit="1"
                    >
                      <i class="el-icon-plus"></i>
                    </el-upload>
                  </el-form-item>
                </el-form>
                <div slot="footer" class="dialog-footer">
                  <el-button @click="nlzs_add_dialogFormVisible = false">取 消</el-button>
                  <el-button type="primary" @click="nlzs_add_handleClose()">确 定</el-button>
                </div>
              </el-dialog>
              <span v-if="shouye_data.ability_display_data.length-1===index">
                <el-button
                  type="primary"
                  icon="el-icon-edit"
                  circle
                  size="mini"
                  @click="nlzs_dialogFormVisible=true;update_nlzs_data(nlzs)"
                ></el-button>
                <el-button
                  type="danger"
                  icon="el-icon-delete"
                  circle
                  size="mini"
                  @click="delete_nlzs(nlzs)"
                ></el-button>
                <el-button type="success" icon="el-icon-plus" circle size="mini" @click="nlzs_add_dialogFormVisible=true"></el-button>
              </span>
              <span v-else>
                <el-button
                  type="primary"
                  icon="el-icon-edit"
                  circle
                  size="mini"
                  @click="nlzs_dialogFormVisible=true;update_nlzs_data(nlzs)"
                ></el-button>
                <el-button
                  type="danger"
                  icon="el-icon-delete"
                  circle
                  size="mini"
                  @click="delete_nlzs(nlzs)"
                ></el-button>
              </span>
            </div>
          </el-form-item>
          <el-form-item label="部分案例">
            <div v-for="(bfal,index) in shouye_data.customer_case_data" :key="o" class="text item">
              {{ bfal.customer_case_data_shop_name}}&nbsp;&nbsp;
              <el-dialog
                title
                :visible.sync="bfal_dialogFormVisible"
              >
                <el-form ref="bfal_form" :model="bfal_form" label-width="80px">
                  <el-form-item label="品牌名">
                    <el-input v-model="bfal_form.customer_case_data_shop_name"></el-input>
                  </el-form-item>
                  <el-form-item label="LOGO">
                    <el-upload
                      action="http://127.0.0.1:8000/app/img_test/"
                      list-type="picture-card"
                      :file-list="bfal_form.customer_case_data_logo"
                      :on-remove="handleRemove"
                      name="image"
                      :on-success="customer_case_data_logo_update"
                      limit="1"
                    >
                      <i class="el-icon-plus"></i>
                    </el-upload>
                  </el-form-item>
                  <el-form-item label="环境">
                    <el-upload
                      action="http://127.0.0.1:8000/app/img_test/"
                      list-type="picture-card"
                      :file-list="bfal_form.customer_case_data_img"
                      :on-success="customer_case_data_img_update"
                      :on-remove="handleRemove"
                      name="image"
                      limit="1"
                    >
                      <i class="el-icon-plus"></i>
                    </el-upload>
                  </el-form-item>
                  <el-form-item label="描述">
                    <quill-editor
                      :content="content"
                      :multiple-limit="1"
                      ref="myQuillEditor"

                      class="editer"
                      :options="editorOption"
                      @blur="onEditorBlur($event)"
                      @focus="onEditorFocus($event)"
                      @change="bfal_form_update_onEditorChange($event)"
                      style="height:100%"
                    ></quill-editor>
                  </el-form-item>
                </el-form>
                <div slot="footer" class="dialog-footer">
                    <el-button @click="bfal_dialogFormVisible=false">取 消</el-button>
                    <el-button type="primary" @click="bfal_handleClose()">确 定</el-button>
                </div>
              </el-dialog>
              <el-dialog
                title
                :visible.sync="bfal_add_dialogFormVisible"
              >
                <el-form ref="bfal_form_add" :model="bfal_form_add" label-width="80px">
                  <el-form-item label="品牌名">
                    <el-input v-model="bfal_form_add.customer_case_data_shop_name"></el-input>
                  </el-form-item>
                  <el-form-item label="LOGO">
                    <el-upload
                      action="http://127.0.0.1:8000/app/img_test/"
                      list-type="picture-card"
                      :file-list="bfal_form_add.customer_case_data_logo"
                      :on-remove="handleRemove"
                      name="image"
                      :on-success="customer_case_data_logo_add"
                      limit="1"
                    >
                      <i class="el-icon-plus"></i>
                    </el-upload>
                  </el-form-item>
                  <el-form-item label="环境">
                    <el-upload
                      action="http://127.0.0.1:8000/app/img_test/"
                      list-type="picture-card"
                      :file-list="bfal_form_add.customer_case_data_img"
                      :on-success="customer_case_data_img_add"
                      :on-remove="handleRemove"
                      name="image"
                      limit="1"
                    >
                      <i class="el-icon-plus"></i>
                    </el-upload>
                  </el-form-item>
                  <el-form-item label="描述">
                    <quill-editor
                      :multiple-limit="1"
                      ref="myQuillEditor"
                      class="editer"
                      :options="editorOption"
                      @blur="onEditorBlur($event)"
                      @focus="onEditorFocus($event)"
                      @change="bfal_form_add_update_onEditorChange($event)"
                      style="height:100%"
                    ></quill-editor>
                  </el-form-item>
                </el-form>
                <div slot="footer" class="dialog-footer">
                    <el-button @click="bfal_add_dialogFormVisible=false">取 消</el-button>
                    <el-button type="primary" @click="bfal_add_handleClose()">确 定</el-button>
                </div>
              </el-dialog>
              <span v-if="shouye_data.customer_case_data.length-1===index">
                <el-button
                  type="primary"
                  icon="el-icon-edit"
                  circle
                  size="mini"
                  @click="update_bfal_data(bfal,index)"
                  ></el-button>
                <el-button
                  type="danger"
                  icon="el-icon-delete"
                  circle
                  size="mini"
                  @click="delete_bfal(bfal,index)"
                  ></el-button>
                <el-button type="success" icon="el-icon-plus" circle size="mini" @click="bfal_add_dialogFormVisible=true"></el-button>
              </span>
              <span v-else>
                <el-button
                  type="primary"
                  icon="el-icon-edit"
                  circle
                  size="mini"
                  @click="update_bfal_data(bfal,index)"
                  ></el-button>
                <el-button
                  type="danger"
                  icon="el-icon-delete"
                  circle
                  size="mini"
                  @click="delete_bfal(bfal,index)"
                  ></el-button>
              </span>
            </div>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="save_shouye_data">立即保存</el-button>
          </el-form-item>
        </el-form>
      </el-tab-pane>
      <el-tab-pane label="职能团队" name="second">职能团队</el-tab-pane>
      <el-tab-pane label="关于我们" name="third">关于我们</el-tab-pane>
      <el-tab-pane label="合作伙伴" name="fourth">合作伙伴</el-tab-pane>
      <el-tab-pane label="联系我们" name="fifth">联系我们</el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import { toggleClass } from "@/utils";
import "@/assets/custom-theme/index.css"; // the theme changed version element-ui css
import {
  quillEditor
} from 'vue-quill-editor'
import 'quill/dist/quill.core.css'
import 'quill/dist/quill.snow.css'
import 'quill/dist/quill.bubble.css'
export default {
  name: "Theme",
  data() {
    return {
      activeName: "first",
      content: '',
      editorOption: {},
      html:'',
      activeName_wntg: "1",
      sdfyd_dialogFormVisible: false,
      nlzs_dialogFormVisible: false,
      bfal_dialogFormVisible: false,
      nlzs_add_dialogFormVisible:false,
      sdfyd_add_dialogFormVisible:false,
      bfal_add_dialogFormVisible:false,
      shouye_data: {
        header_text: "帮商户做好生意",
        header_img: [{name:'header_img.jpg',url:'http://127.0.0.1:8000/media/1.jpg'}],
        for_you: "为您提供",
        for_you_data: [
          {
            for_you_data_img: [{name:'header_img.jpg',url:'http://127.0.0.1:8000/media/1.jpg'}],
            for_you_data_title: "统筹规划",
            for_you_data_text:
              "周边及行业数据调查，门店线上过往数据分析，门店整体运营思路"
          },
          {
            for_you_data_img: [{name:'header_img.jpg',url:'http://127.0.0.1:8000/media/1.jpg'}],
            for_you_data_title: "线上执行",
            for_you_data_text: "套餐品项设立，页面视觉包装，后台维护更新"
          },
          {
            for_you_data_img: [{name:'header_img.jpg',url:'http://127.0.0.1:8000/media/1.jpg'}],
            for_you_data_title: "线下培训",
            for_you_data_text:
              "技师培训-线上评论认知及职能团队，店长培训-线上运营管理，经理培训-指标拆解方案"
          },
          {
            for_you_data_img:
              [{name:'header_img.jpg',url:'http://127.0.0.1:8000/media/1.jpg'}],
            for_you_data_title: "营销活动运营",
            for_you_data_text: "拼团活动，产品立减，秒杀活动，抵用券"
          },
          {
            for_you_data_img: [{name:'header_img.jpg',url:'http://127.0.0.1:8000/media/1.jpg'}],
            for_you_data_title: "数据分析咨询",
            for_you_data_text:
              "提供合作周期门店趋势分析，根据行业、商圈进行数据整合调整运营方向，月度指标拆解及完成率阶段提醒，提供竞对分析，提升自身能力值，并持续追踪。"
          }
        ],
        ability_display: "能力展示",
        ability_display_data: [
          {
            ability_display_img: [{name:'header_img.jpg',url:'http://127.0.0.1:8000/media/1.jpg'}],
            ability_display_title: "品牌营销"
          },
          {
            ability_display_img:
              [{name:'header_img.jpg',url:'http://127.0.0.1:8000/media/1.jpg'}],
            ability_display_title: "数据运营"
          },
          {
            ability_display_img: [{name:'header_img.jpg',url:'http://127.0.0.1:8000/media/1.jpg'}],
            ability_display_title: "商务拓展"
          },
          {
            ability_display_img: [{name:'header_img.jpg',url:'http://127.0.0.1:8000/media/1.jpg'}],
            ability_display_title: "培训"
          }
        ],
        customer_case: "部分案例",
        customer_case_data: [
          {
            customer_case_data_logo: [{name:'header_img.jpg',url:'http://127.0.0.1:8000/media/1.jpg'}],
            customer_case_data_shop_name: "iSpa",
            customer_case_data_img: [{name:'header_img.jpg',url:'http://127.0.0.1:8000/media/1.jpg'}],
            customer_case_data_text:
              '<div style=""><div><p><span style="">iSpa是北京第一家泰国大使馆认证的泰式SPA。是中国境内唯一同时获得JW万豪、希尔顿、洲际、威斯汀、君悦、康莱德、安达仕几大酒店品牌进驻许可的SPA品牌，目前在全国核心城市共计约50多家五星级酒店开设直营专属SPA馆。服务iSpa集团旗下iSpa、影逸SPA、泰美好SPA品牌门店共计50+门店，覆盖城市北京、上海、广州、深圳、成都、武汉、苏州、天津、青岛、三亚等。</span></p><p><span style="">2019年年度数据</span></p><p><span style="">线上核销金额破<font color="#ff0000"><b>10,000,000RMB</b></font></span></p><p><span style="">线上核销团单破<font color="#ff0000"><b>20,000+</b></font><br></span></p></div></div>'
          },
          {
            customer_case_data_logo: [{name:'header_img.jpg',url:'http://127.0.0.1:8000/media/1.jpg'}],
            customer_case_data_shop_name: "Lily Nails",
            customer_case_data_img: [{name:'header_img.jpg',url:'http://127.0.0.1:8000/media/1.jpg'}],
            customer_case_data_text:
              "LILYNAILS创立于2001年，19年来在北京、上海等城市开放17家直营门店，已为100万都市人群提供高端私人美业服务，旗下业务涵盖美甲、美睫、美肤、脱毛、纤体、纹绣等垂直细分领域，合作伙伴包括法国航空、德国航空、DIOR迪奥等一线大牌。时尚杂志悦己、瑞丽、PCLADY等亦对其进行过深入报道。"
          },
          {
            customer_case_data_logo: [{name:'header_img.jpg',url:'http://127.0.0.1:8000/media/1.jpg'}],
            customer_case_data_shop_name: "Face·K",
            customer_case_data_img: [{name:'header_img.jpg',url:'http://127.0.0.1:8000/media/1.jpg'}],
            customer_case_data_text:
              "FaceK将头发管理从美发行业中摘离出来，与美肤项目整合，突破传统的美发+美容“综合店”的模式，打造了一种全新玩法，并创造了高流量，在高客单价和经营效率上均可圈可点。"
          },
          {
            customer_case_data_logo: [{name:'header_img.jpg',url:'http://127.0.0.1:8000/media/1.jpg'}],
            customer_case_data_shop_name: "Mirror Mirror魔镜",
            customer_case_data_img: [{name:'header_img.jpg',url:'http://127.0.0.1:8000/media/1.jpg'}],
            customer_case_data_text:
              "MirrorMirror魔镜美甲北京三里屯名媛必选美甲店，高端日式风格，客户覆盖北京名媛圈、网红圈、高阶白领等中高层消费人群。品牌创始人毕业于北京电影学院美术系，美感创新能力天赋异禀。两年打造4家门店。"
          }
        ],
        menu:
          '<a class="header__menu__item activity" href="/">首页</a><a class="header__menu__item" href="platform/data_service.html">职能团队</a><a class="header__menu__item" href="platform/about.html">关于我们</a><a class="header__menu__item" href="platform/customer_case.html">合作伙伴</a><a class="header__menu__item" href="platform/contact_us.html">联系我们</a>'
      },
      dialogImageUrl:
        "D:\\PythonProject\\beiaikeji_official_website\\image\\hero-back.jpg",
      dialogVisible: false,
      shouye_wntg: false,
      shouye_form: {
        shouye_title: "帮商户做好生意",
        region: "",
        date1: "",
        date2: "",
        delivery: false,
        type: [],
        resource: "",
        desc: ""
      },
      sdfyd_form: {
        for_you_data_img: "",
        for_you_data_title: "",
        for_you_data_text: "",
        index: ""
      },
      bfal_form_add:{
        customer_case_data_logo: [],
        customer_case_data_img: [],
        customer_case_data_text: "",
        customer_case_data_shop_name: "",
      },
      sdfyd_form_add:{
        for_you_data_img: [{name: "food.jpeg",url:""}],
        for_you_data_title: "",
        for_you_data_text: ''
      },
      bfal_form: {
        customer_case_data_logo: [{name: "food.jpeg",url:""}],
        customer_case_data_img: [{name: "food.jpeg",url:""}],
        customer_case_data_text: "",
        customer_case_data_shop_name: "",
        index: ""
      },
      nlzs_form: {
        ability_display_img: [{name: "food.jpeg",url:"https://www.google.cn/chrome/static/images/hero-back-large-desktop.jpg"}],
        index: "",
        ability_display_title: ""
      },
      nlzs_form_add:{
        ability_display_img: [{name: "food.jpeg",url:""}],
        ability_display_title: ""
      },
      fileList: [
        {
          name: "food.jpeg",
          url:
            "http://127.0.0.1:8000/media/1.jpg"
        }
      ],
      banner:[],
      customer_case_data_logo:[],
      customer_case_data_img: []
    };
  },
  created: function() {
  },
  methods: {
    //头图更换
    header_img(response, file, fileList){
      this.shouye_form.header_img = "http://127.0.0.1:8000/media/"+response
      this.shouye_data.header_img[0].url = "http://127.0.0.1:8000/media/"+response
      console.log(this.shouye_data)
    },
    //编辑为您提供上传图片
    sdfyd_form_img(response, file, fileList){
        this.sdfyd_form.for_you_data_img[0].url = "http://127.0.0.1:8000/media/"+response
    },
    //添加图片
    sdfyd_form_add_img(response, file, fileList){
        this.sdfyd_form_add.for_you_data_img[0].url = "http://127.0.0.1:8000/media/"+response
    },
    bfal_add_handleClose(){
      console.log(this.bfal_form_add)
      this.bfal_add_dialogFormVisible = false;
      this.shouye_data.customer_case_data.push({
        "customer_case_data_shop_name":this.bfal_form_add.customer_case_data_shop_name,
        "customer_case_data_text":this.bfal_form_add.customer_case_data_text,
        "customer_case_data_img":this.bfal_form_add.customer_case_data_img,
        "customer_case_data_logo":this.bfal_form_add.customer_case_data_logo
      })
    },
    //能力展示编辑
    nlzs_form_img(response, file, fileList){
        this.nlzs_form.ability_display_img[0].url = "http://127.0.0.1:8000/media/"+response
    },
    //添加能力展示图片
    nlzs_form_img_add(response, file, fileList){
        this.nlzs_form_add.ability_display_img[0].url = "http://127.0.0.1:8000/media/"+response
    },
    customer_case_data_logo_update(response, file, fileList){
        this.bfal_form.customer_case_data_logo[0].url = "http://127.0.0.1:8000/media/"+response
    },
    customer_case_data_img_update(response, file, fileList){
        this.bfal_form.customer_case_data_img[0].url = "http://127.0.0.1:8000/media/"+response
    },
    customer_case_data_logo_add(response, file, fileList){
        this.bfal_form_add.customer_case_data_logo = [{name: "food.jpeg",url:"http://127.0.0.1:8000/media/"+response}]
    },
    customer_case_data_img_add(response, file, fileList){
        this.bfal_form_add.customer_case_data_img = [{name: "food.jpeg",url:"http://127.0.0.1:8000/media/"+response}]
    },
    handlePictureCardPreview(file) {
      this.dialogImageUrl = file.url;
      this.dialogVisible = true;
      console.log(this.dialogImageUrl);
    },
    //for_you删除为您提供数据
    delete_for_you(item) {
      this.$confirm("确定要删除吗? 是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning"
      }).then(() => {
        var index = this.shouye_data.for_you_data.indexOf(item);
        // delete this.shouye_data.for_you_data[index]
        if (index !== -1) {
          this.shouye_data.for_you_data.splice(index, 1);
        }
      });
    },
    //nlzs删除能力展示数据
    delete_nlzs(item) {
      this.$confirm("确定要删除吗? 是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning"
      }).then(() => {
        var index = this.shouye_data.ability_display_data.indexOf(item);
        // delete this.shouye_data.for_you_data[index]
        if (index !== -1) {
          this.shouye_data.ability_display_data.splice(index, 1);
        }
      });
    },
    //bfal删除部分案例数据
    delete_bfal(item) {
      this.$confirm("确定要删除吗? 是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning"
      }).then(() => {
        var index = this.shouye_data.customer_case_data.indexOf(item);
        // delete this.shouye_data.for_you_data[index]
        if (index !== -1) {
          this.shouye_data.customer_case_data.splice(index, 1);
        }
      });
    },
    //for_you更改为您提供数据
    update_for_you_data(item,index) {
      this.sdfyd_dialogFormVisible = true;
      this.sdfyd_form.for_you_data_text = item.for_you_data_text
      this.sdfyd_form.for_you_data_title = item.for_you_data_title
      this.sdfyd_form.for_you_data_img = item.for_you_data_img
      this.sdfyd_form.index = index
    },
    //nlzs更改能力展示数据
    update_nlzs_data(item) {
      var index = this.shouye_data.ability_display_data.indexOf(item);
      this.nlzs_form.ability_display_title = this.shouye_data.ability_display_data[index].ability_display_title;
      this.nlzs_form.ability_display_img = this.shouye_data.ability_display_data[index].ability_display_img;
      this.nlzs_form.index = index;
    },
    //bfal更改部分案例数据
    update_bfal_data(item,index) {
      this.bfal_dialogFormVisible = true;
      this.bfal_form.customer_case_data_shop_name = item.customer_case_data_shop_name;
      this.bfal_form.customer_case_data_logo=item.customer_case_data_logo;
      this.bfal_form.customer_case_data_text = item.customer_case_data_text;
      this.content = item.customer_case_data_text
      this.bfal_form.customer_case_data_img=item.customer_case_data_img;
      this.bfal_form.index = index
      console.log(this.bfal_form.index)
    },
    //for_you模拟框关闭前回调
    sdfyd_handleClose() {
      this.sdfyd_dialogFormVisible = false;
      console.log(this.sdfyd_form.index)
      this.shouye_data.for_you_data[this.sdfyd_form.index].for_you_data_title = this.sdfyd_form.for_you_data_title;
      this.shouye_data.for_you_data[this.sdfyd_form.index].for_you_data_text = this.sdfyd_form.for_you_data_text;
      this.shouye_data.for_you_data[this.sdfyd_form.index].for_you_data_img = this.sdfyd_form.for_you_data_img;
    },
    sdfyd_add_handleClose(){
      this.sdfyd_add_dialogFormVisible = false;
      this.shouye_data.for_you_data.push({
          "for_you_data_title":this.sdfyd_form_add.for_you_data_title,
          "for_you_data_text":this.sdfyd_form_add.for_you_data_text,
          "for_you_data_img":this.sdfyd_form_add.for_you_data_img
      })
    },
    //nlzs模拟框关闭前回调
    nlzs_handleClose() {
      this.nlzs_dialogFormVisible = false;
      this.shouye_data.ability_display_data[this.nlzs_form.index].ability_display_title = this.nlzs_form.ability_display_title;
      this.shouye_data.ability_display_data[this.nlzs_form.index].ability_display_img = this.nlzs_form.ability_display_img;
    },
    nlzs_add_handleClose(){
      this.nlzs_add_dialogFormVisible = false;
      this.shouye_data.ability_display_data.push({
          "ability_display_title":this.nlzs_form_add.ability_display_title,
          "ability_display_img":this.nlzs_form_add.ability_display_img
      })
    },
    //bfal模拟框关闭之前回调
    bfal_handleClose() {
      this.bfal_dialogFormVisible = false;
      this.shouye_data.customer_case_data[this.bfal_form.index].customer_case_data_shop_name = this.bfal_form.customer_case_data_shop_name;
      this.shouye_data.customer_case_data[this.bfal_form.index].customer_case_data_logo_list = this.bfal_form.customer_case_data_logo_list;
      this.shouye_data.customer_case_data[this.bfal_form.index].customer_case_data_text = this.bfal_form.customer_case_data_text;
      this.shouye_data.customer_case_data[this.bfal_form.index].customer_case_data_img_list = this.bfal_form.customer_case_data_img_list;
    },
    bfal_form_add_update_onEditorChange({ editor, html, text }){
      this.bfal_form_add.customer_case_data_text = html
    },
    onEditorBlur(editor) {
      //失去焦点事件
    },
    onEditorFocus(editor) {
      //获得焦点事件
    },
    bfal_form_update_onEditorChange({ editor, html, text }) {
      this.bfal_form.customer_case_data_text = html
    },
    change(val) {
      console.log(val);
    },
    setImgInfo(response, file, fileList){
      console.log('1')
      console.log(response)
    },
    save_shouye_data(){
      this.axios
        .get('http://127.0.0.1:8000/app/save_shouye_data/', {
          params: {
            // 每页显示的条数
            shouye_data: this.shouye_data
          }
        })
        .then(res => {
          // this.business_districts = res.data.data
          if (res.data.code == 0){
            this.$notify({
              title: '成功',
              message: '保存成功',
              type: 'success'
            });
          }
        })
        .catch(function(error) {
          this.loading = false
          console.log(error)
        })
    }
  },
  computed: {
    editor() {
        return this.$refs.myQuillEditor.quill;
    },
  }
};
</script>

<style scoped>
.field-label {
  vertical-align: middle;
}

.box-card {
  width: 400px;
  max-width: 100%;
  margin: 20px auto;
}

.block {
  padding: 30px 24px;
}

.tag-item {
  margin-right: 15px;
}
</style>
