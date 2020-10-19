<template>
  <div class="app-container">
    <el-tabs
      v-model="activeName"
      style="margin-left:15px;margin-top:15px;"
      @tab-click="handleClick"
    >
      <el-tab-pane label="客户CRM" name="first"
      >
        <el-form
          ref="dynamicValidateForm"
          :model="dynamicValidateForm"
          label-width="100px"
          style="margin-top:25px;"
          class="demo-dynamic"
        >
          <el-form-item
            v-for="(domain, index) in dynamicValidateForm"
            :key="domain.key"
            :label="domain.label"
            style="width:50%"
            :prop="'domains.' + index + '.value'"
          >
            <span v-if="domain.type === '文本类型'">
              <el-input style="width:35%" />
            </span>
            <span v-if="domain.type === '日期类型'">
              <el-date-picker />
            </span>
            <span v-if="domain.type === '选择下拉框'">
              <el-select>
                <el-option
                  v-for="item in domain.select"
                  :key="item.label"
                  :label="item.label"
                  :value="item"
                />
              </el-select>
            </span>
            <span v-if="domain.type === '大文本框'">
              <el-input type="textarea" />
            </span>
            <el-button @click.prevent="removeDomain(domain)">删除</el-button>
            <el-button @click.prevent="dialogFormVisible_edit = true;editDomain(domain)">编辑</el-button>
          </el-form-item>
          <el-form-item>
            <el-button type="success" @click="submitForm">提交</el-button>
            <el-button type="primary" @click="dialogFormVisible = true">新增</el-button>
          </el-form-item>
        </el-form>
      </el-tab-pane>
      <el-tab-pane label="订单管理" name="second">
        <el-form
          ref="order_dynamicValidateForm"
          :model="order_dynamicValidateForm"
          label-width="100px"
          style="margin-top:25px;"
          class="demo-dynamic"
        >
          <el-form-item
            v-for="(domain, index) in order_dynamicValidateForm"
            :key="domain.key"
            :label="domain.label"
            style="width:50%"
            :prop="'domains.' + index + '.value'"
          >
            <span v-if="domain.type === '文本类型'">
              <el-input style="width:35%" />
            </span>
            <span v-if="domain.type === '日期类型'">
              <el-date-picker />
            </span>
            <span v-if="domain.type === '选择下拉框'">
              <el-select>
                <el-option
                  v-for="item in domain.select"
                  :key="item.label"
                  :label="item.label"
                  :value="item"
                />
              </el-select>
            </span>
            <span v-if="domain.type === '大文本框'">
              <el-input type="textarea" />
            </span>
            <el-button @click.prevent="order_removeDomain(domain)">删除</el-button>
            <el-button
              @click.prevent="order_dialogFormVisible_edit = true;order_editDomain(domain)"
            >编辑</el-button>
          </el-form-item>
          <el-form-item>
            <el-button type="success" @click="order_submitForm">提交</el-button>
            <el-button type="primary" @click="order_dialogFormVisible = true">新增</el-button>
          </el-form-item>
        </el-form>
      </el-tab-pane>
      <el-tab-pane label="销售待办事项" name="third">
        <el-form
          ref="to_do_dynamicValidateForm"
          :model="to_do_dynamicValidateForm"
          label-width="100px"
          style="margin-top:25px;"
          class="demo-dynamic"
        >
          <el-form-item
            v-for="(domain, index) in to_do_dynamicValidateForm"
            :key="domain.name"
            style="width:50%"
            :prop="'domains.' + index + '.value'"
          >
            任务：{{ domain.name }}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{{ domain.select }}：{{ domain.time }}天
            <el-button @click.prevent="todo_removeDomain(domain)">删除</el-button>
            <el-button
              @click.prevent="todo_dialogFormVisible_edit = true;todo_editDomain(domain)"
            >编辑</el-button>
          </el-form-item>
          <el-form-item>
            <el-button type="success" @click="todo_submitForm">提交</el-button>
            <el-button type="primary" @click="todo_dialogFormVisible = true">新增</el-button>
          </el-form-item>
        </el-form>
      </el-tab-pane>
      <el-tab-pane label="提成点设置" name="fourth">
        <el-form
          ref="commission_dynamicValidateForm"
          :model="commission_dynamicValidateForm"
          label-width="100px"
          style="margin-top:25px;"
          class="demo-dynamic"
        >
          <el-form-item
            v-for="(domain, index) in commission_dynamicValidateForm"
            :key="domain.commission_performance"
            style="width:50%"
            :prop="'domains.' + index + '.value'"
          >
            业绩>={{ domain.commission_performance }}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;提成点：{{ domain.commission_commission_point }} %
            <el-button @click.prevent="commission_removeDomain(domain)">删除</el-button>
            <el-button
              @click.prevent="commission_dialogFormVisible_edit = true;commission_editDomain(domain)"
            >编辑</el-button>
          </el-form-item>
          <el-form-item>
            <el-button type="success" @click="commission_submitForm">提交</el-button>
            <el-button type="primary" @click="commission_dialogFormVisible = true">新增</el-button>
          </el-form-item>
        </el-form>
      </el-tab-pane>
      <el-tab-pane label="私海设置" name="five">
        <el-form>
          <el-form-item label="存放时间" label-width="100px">
            <el-slider
              v-model="private_sea_time"
              :min="1"
              :max="10000"
              show-input
              style="width:50%"
            />
          </el-form-item>
          <el-form-item label="存放数量" label-width="100px">
            <el-slider
              v-model="private_sea_length"
              :min="1"
              :max="10000"
              show-input
              style="width:50%"
            />
          </el-form-item>
          <el-form-item>
            <el-button type="success" @click="private_sea_edit">提交</el-button>
          </el-form-item>
        </el-form>
      </el-tab-pane>
      <el-tab-pane label="用户管理" name="six">
        <el-form>
          <el-button
            type="primary"
            style="margin-left:15px;margin-right:30px"
            @click="create_group = true"
          >添加销售组</el-button>
          <el-button
            type="primary"
            style="margin-left:15px;margin-right:30px"
            @click="create_user_data = true"
          >添加用户</el-button>
          <el-table
            ref="multipleTable"
            v-loading="loading"
            :data="tableData"
            border
            fit
            stripe
            highlight-current-row
            style="width: 100%;margin-left:15px;margin-right:30px"
          >
            <el-table-column prop="username" label="用户名" show-overflow-tooltip />
            <el-table-column prop="first_name" label="姓名" show-overflow-tooltip />
            <el-table-column prop="group" label="组名" show-overflow-tooltip />
            <el-table-column prop="avatar" label="角色" show-overflow-tooltip />
            <el-table-column label="操作" width="210" :show-overflow-tooltip="true">
              <template slot-scope="scope">
                <div v-if="scope.row.avatar === '销售' || scope.row.avatar === 'admin'">
                  <el-tooltip class="item" effect="dark" content="删除" placement="top-start">
                    <el-button
                      size="mini"
                      type="danger"
                      content="删除"
                      placement="top"
                      @click="delete_user(scope.row)"
                    >
                      <i class="el-icon-close" />
                    </el-button>
                  </el-tooltip>
                  <el-tooltip class="item" effect="dark" content="修改" placement="top-start">
                    <el-button
                        size="mini"
                        type="primary"
                        content="修改"
                        placement="top"
                        @click="update_user(scope.row);update_user_data_data=true"
                      >
                        <svg-icon icon-class="edit" />
                      </el-button>
                  </el-tooltip>
                </div>
              </template>
            </el-table-column>
          </el-table>
        </el-form>
      </el-tab-pane>
    </el-tabs>
    <el-dialog title="客户CRM新增字段" :visible.sync="dialogFormVisible">
      <el-form ref="form" :model="form" :rules="rules">
        <el-form-item label="字段名称" :label-width="formLabelWidth">
          <el-input v-model="form.name" autocomplete="off" style="width:50%" />
        </el-form-item>
        <el-form-item label="字段类型" :label-width="formLabelWidth">
          <el-select
            v-model="form.type"
            placeholder="请选择字段类型"
            style="width:50%"
            @change="selectform"
          >
            <el-option label="文本类型" value="文本类型" />
            <el-option label="日期类型" value="日期类型" />
            <el-option label="选择下拉框" value="选择下拉框" />
            <el-option label="大文本框" value="大文本框" />
          </el-select>
          <el-form-item
            v-for="(domain, index) in select_Form"
            :key="domain.key"
            style="width:50%"
            :prop="'domains.' + index + '.value'"
          >
            <el-input v-model="domain.label" :disabled="true" style="width:50%" />
            <!-- <el-button><i class="el-icon-plus" /></el-button> -->
            <el-button @click.prevent="select_removeDomain(domain)">删除</el-button>
          </el-form-item>
          <el-form-item v-for="(i, index1) in add_setting" :key="index1" style="width:50%">
            <el-input v-model="form.select_text" style="width:50%" @change="add_select_form" />
            <el-button>添加</el-button>
          </el-form-item>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="addDomain();dialogFormVisible = false">确 定</el-button>
      </div>
    </el-dialog>
    <el-dialog title="客户CRM编辑字段" :visible.sync="dialogFormVisible_edit">
      <el-form :model="form">
        <el-form-item label="字段名称" :label-width="formLabelWidth">
          <el-input v-model="form.name" autocomplete="off" style="width:50%" />
        </el-form-item>
        <el-form-item label="字段类型" :label-width="formLabelWidth">
          <el-select
            v-model="form.type"
            placeholder="请选择字段类型"
            style="width:50%"
            @change="selectform"
          >
            <el-option label="文本类型" value="文本类型" />
            <el-option label="日期类型" value="日期类型" />
            <el-option label="选择下拉框" value="选择下拉框" />
            <el-option label="大文本框" value="大文本框" />
          </el-select>
          <el-form-item
            v-for="(domain, index) in select_Form"
            :key="domain.key"
            style="width:50%"
            :prop="'domains.' + index + '.value'"
          >
            <el-input v-model="domain.label" :disabled="true" style="width:50%" />
            <!-- <el-button><i class="el-icon-plus" /></el-button> -->
            <el-button @click.prevent="select_removeDomain(domain)">删除</el-button>
          </el-form-item>
          <el-form-item v-for="(i, index1) in add_setting" :key="index1" style="width:50%">
            <el-input v-model="form.select_text" style="width:50%" @change="add_select_form" />
            <el-button>添加</el-button>
          </el-form-item>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible_edit = false">取 消</el-button>
        <el-button type="primary" @click="editForm();dialogFormVisible_edit = false">确 定</el-button>
      </div>
    </el-dialog>
    <el-dialog title="订单管理新增字段" :visible.sync="order_dialogFormVisible">
      <el-form ref="form" :model="form" :rules="rules">
        <el-form-item label="字段名称" :label-width="formLabelWidth">
          <el-input v-model="form.order_name" autocomplete="off" style="width:50%" />
        </el-form-item>
        <el-form-item label="字段类型" :label-width="formLabelWidth">
          <el-select
            v-model="form.order_type"
            placeholder="请选择字段类型"
            style="width:50%"
            @change="order_selectform"
          >
            <el-option label="文本类型" value="文本类型" />
            <el-option label="日期类型" value="日期类型" />
            <el-option label="选择下拉框" value="选择下拉框" />
            <el-option label="大文本框" value="大文本框" />
          </el-select>
          <el-form-item
            v-for="(domain, index) in order_select_Form"
            :key="domain.key"
            style="width:50%"
            :prop="'domains.' + index + '.value'"
          >
            <el-input v-model="domain.label" :disabled="true" style="width:50%" />
            <!-- <el-button><i class="el-icon-plus" /></el-button> -->
            <el-button @click.prevent="select_removeDomain(domain)">删除</el-button>
          </el-form-item>
          <el-form-item v-for="(i, index1) in order_add_setting" :key="index1" style="width:50%">
            <el-input
              v-model="form.order_select_text"
              style="width:50%"
              @change="order_add_select_form"
            />
            <el-button>添加</el-button>
          </el-form-item>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="order_dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="order_addDomain();order_dialogFormVisible = false">确 定</el-button>
      </div>
    </el-dialog>
    <el-dialog title="订单管理编辑字段" :visible.sync="order_dialogFormVisible_edit">
      <el-form :model="form">
        <el-form-item label="字段名称" :label-width="formLabelWidth">
          <el-input v-model="form.order_name" autocomplete="off" style="width:50%" />
        </el-form-item>
        <el-form-item label="字段类型" :label-width="formLabelWidth">
          <el-select
            v-model="form.order_type"
            placeholder="请选择字段类型"
            style="width:50%"
            @change="order_selectform"
          >
            <el-option label="文本类型" value="文本类型" />
            <el-option label="日期类型" value="日期类型" />
            <el-option label="选择下拉框" value="选择下拉框" />
            <el-option label="大文本框" value="大文本框" />
          </el-select>
          <el-form-item
            v-for="(domain, index) in order_select_Form"
            :key="domain.key"
            style="width:50%"
            :prop="'domains.' + index + '.value'"
          >
            <el-input v-model="domain.label" :disabled="true" style="width:50%" />
            <!-- <el-button><i class="el-icon-plus" /></el-button> -->
            <el-button @click.prevent="order_select_removeDomain(domain)">删除</el-button>
          </el-form-item>
          <el-form-item v-for="(i, index1) in order_add_setting" :key="index1" style="width:50%">
            <el-input
              v-model="form.order_select_text"
              style="width:50%"
              @change="order_add_select_form"
            />
            <el-button>添加</el-button>
          </el-form-item>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="order_dialogFormVisible_edit = false">取 消</el-button>
        <el-button type="primary" @click="order_editForm();order_dialogFormVisible_edit = false">确 定</el-button>
      </div>
    </el-dialog>
    <el-dialog title="销售任务事项：新增任务" :visible.sync="todo_dialogFormVisible">
      <el-form ref="form" :model="form" :rules="rules">
        <el-form-item label="任务名称" :label-width="formLabelWidth">
          <el-input v-model="form.to_do_name" autocomplete="off" style="width:50%" />
        </el-form-item>
        <el-form-item label="任务类型" :label-width="formLabelWidth">
          <el-select v-model="form.select" placeholder="请选段类型" @change="todo_SelectForm">
            <el-option label="单次任务" value="单次任务" />
            <el-option label="重复任务" value="重复任务" />
          </el-select>
        </el-form-item>
        <el-form-item v-for="(i, index1) in todo_add_setting" :key="index1" label="截止时间(天)">
          <el-input
            v-model="form.to_do_time"
            autocomplete="off"
            placeholder="项目开始后多长时间内完成"
            style="width:50%"
          />
        </el-form-item>
        <el-form-item v-for="(i, index1) in todo_add_setting2" :key="index1" label="重复时间(天)">
          <el-input
            v-model="form.to_do_time"
            autocomplete="off"
            placeholder="项目开始后多长时间内重复一次"
            style="width:50%"
          />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="todo_dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="todo_addDomain();todo_dialogFormVisible = false">确 定</el-button>
      </div>
    </el-dialog>
    <el-dialog title="销售任务事项：编辑任务" :visible.sync="todo_dialogFormVisible_edit">
      <el-form ref="form" :model="form" :rules="rules">
        <el-form-item label="任务名称" :label-width="formLabelWidth">
          <el-input v-model="form.to_do_name" autocomplete="off" style="width:50%" />
        </el-form-item>
        <el-form-item label="任务类型" :label-width="formLabelWidth">
          <el-select v-model="form.select" placeholder="请选段类型" @change="todo_SelectForm">
            <el-option label="单次任务" value="单次任务" />
            <el-option label="重复任务" value="重复任务" />
          </el-select>
        </el-form-item>
        <el-form-item v-for="(i, index1) in todo_add_setting" :key="index1" label="截止时间(天)">
          <el-input
            v-model="form.to_do_time"
            autocomplete="off"
            placeholder="项目开始后多长时间内完成"
            style="width:50%"
          />
        </el-form-item>
        <el-form-item v-for="(i, index1) in todo_add_setting2" :key="index1" label="重复时间(天)">
          <el-input
            v-model="form.to_do_time"
            autocomplete="off"
            placeholder="项目开始后多长时间内重复一次"
            style="width:50%"
          />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="todo_dialogFormVisible_edit = false">取 消</el-button>
        <el-button type="primary" @click="todo_editForm();todo_dialogFormVisible_edit = false">确 定</el-button>
      </div>
    </el-dialog>
    <el-dialog title="提成点设置:新增提成点" :visible.sync="commission_dialogFormVisible">
      <el-form ref="form" :model="form" :rules="rules">
        <el-form-item label="业绩＞=" :label-width="formLabelWidth">
          <el-input v-model="form.commission_performance" autocomplete="off" style="width:50%" />
        </el-form-item>
        <el-form-item label="提成点" :label-width="formLabelWidth">
          <el-input-number v-model="form.commission_commission_point" size="mini" />&nbsp;&nbsp;&nbsp;%
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="commission_dialogFormVisible = false">取 消</el-button>
        <el-button
          type="primary"
          @click="commission_addDomain();commission_dialogFormVisible = false"
        >确 定</el-button>
      </div>
    </el-dialog>
    <el-dialog title="提成点设置:编辑提成点" :visible.sync="commission_dialogFormVisible_edit">
      <el-form ref="form" :model="form" :rules="rules">
        <el-form-item label="业绩＞" :label-width="formLabelWidth">
          <el-input v-model="form.commission_performance" autocomplete="off" style="width:50%" />
        </el-form-item>
        <el-form-item label="提成点" :label-width="formLabelWidth">
          <el-input-number v-model="form.commission_commission_point" size="mini" />&nbsp;&nbsp;&nbsp;%
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="commission_dialogFormVisible_edit = false">取 消</el-button>
        <el-button
          type="primary"
          @click="commission_editForm();commission_dialogFormVisible_edit = false"
        >确 定</el-button>
      </div>
    </el-dialog>
    <el-dialog title="添加销售" :visible.sync="create_user_data">
      <el-form ref="form" :model="form" :rules="rules">
        <el-form-item label="用户名" :label-width="formLabelWidth">
          <el-input v-model="form.username" autocomplete="off" style="width:50%" />
        </el-form-item>
        <el-form-item label="姓名" :label-width="formLabelWidth">
          <el-input v-model="form.first_name" autocomplete="off" style="width:50%" />
        </el-form-item>
        <el-form-item label="角色" :label-width="formLabelWidth">
          <el-select v-model="form.avatar" placeholder="请选择角色" style="width:50%">
            <el-option label="admin" value="admin" />
            <el-option label="销售" value="销售" />
          </el-select>
        </el-form-item>
        <el-form-item label="小组" :label-width="formLabelWidth">
            <el-select v-model="form.group" placeholder="请选择">
              <el-option
                v-for="item in group_data"
                :key="item.id"
                :label="item.label"
                :value="item.id">
              </el-option>
            </el-select>
          </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="create_user_data = false">取 消</el-button>
        <el-button type="primary" @click="create_user();create_user_data = false">确 定</el-button>
      </div>
    </el-dialog>
    <el-dialog title="添加销售组" :visible.sync="create_group">
        <el-form ref="form" :model="form" :rules="rules">
          <el-form-item label="组名" :label-width="formLabelWidth">
            <el-input v-model="form.group_name" autocomplete="off" style="width:50%" />
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="create_group = false">取 消</el-button>
          <el-button type="primary" @click="create_group_name();create_group = false">确 定</el-button>
        </div>
    </el-dialog>
    <el-dialog title="编辑销售" :visible.sync="update_user_data_data">
      <el-form ref="form" :model="update_user_data" :rules="rules">
          <el-form-item label="用户名" :label-width="formLabelWidth">
            <el-input v-model="update_user_data.username" autocomplete="off" style="width:50%" :disabled="true"/>
          </el-form-item>
          <el-form-item label="姓名" :label-width="formLabelWidth">
            <el-input v-model="update_user_data.first_name" autocomplete="off" style="width:50%" :disabled="true"/>
          </el-form-item>
          <el-form-item label="姓名" :label-width="formLabelWidth">
            <el-select v-model="update_user_data.avatar" style="width:50%">
              <el-option label="admin" value="admin" />
              <el-option label="销售" value="销售" />
            </el-select>
          </el-form-item>
          <el-form-item label="小组" :label-width="formLabelWidth">
            <el-select v-model="update_user_data.group" placeholder="请选择">
              <el-option
                v-for="item in group_data"
                :key="item.id"
                :label="item.label"
                :value="item.id">
              </el-option>
            </el-select>
          </el-form-item>
        </el-form>
      <div slot="footer" class="dialog-footer">
          <el-button @click="update_user_data_data = false">取 消</el-button>
          <el-button type="primary" @click="update_user_data_yes();update_user_data_data = false">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import global from '@/store/modules/user'

export default {
  data() {
    return {
      activeName: 'first',
      dynamicValidateForm: [],
      order_dynamicValidateForm: [],
      to_do_dynamicValidateForm: [],
      update_user_data_data: false,
      create_user_data:false,
      create_group: false,
      commission_dynamicValidateForm: [],
      select: [],
      select_Form: [],
      order_select_Form: [],
      todo_select_Form: [],
      commission_select_Form: [],
      add_setting: '',
      order_add_setting: '',
      dialogTableVisible: false,
      todo_add_setting: '',
      dialogFormVisible_edit: false,
      dialogFormVisible: false,
      todo_dialogFormVisible: false,
      todo_dialogFormVisible_edit: false,
      order_dialogFormVisible: false,
      private_sea_time: 0,
      private_sea_length: 0,
      order_dialogFormVisible_edit: false,
      commission_dialogFormVisible: false,
      commission_dialogFormVisible_edit: false,
      tableData: [],
      total: 0,
      pagesize: 10,
      currentPage: 1,
      form: {
        order_name: '',
        username: '',
        first_name: '',
        avatar: '',
        order_type: [],
        order_index: [],
        to_do_name: '',
        to_do_time: '',
        to_do_index: '',
        group:'',
        commission_performance: '',
        commission_commission_point: '',
        commission_index: '',
        name: '',
        region: '',
        index: '',
        date1: '',
        date2: '',
        group_name:'',
        delivery: false,
        type: [],
        resource: '',
        desc: '',
        select: '',
        select_text: '',
        order_select_text: ''
      },
      update_user_data:{
        username:'',
        first_name:'',
        avatar:'',
        group:'',
      },
      avatar:[{'id':'销售','label':'销售'},{'id':'admin','label':'admin'}],
      group_data:[],
      rules: {
        name1: [{ required: true, message: '请输入字段名称', trigger: 'blur' }],
        region: [
          { required: true, message: '请选择活动区域', trigger: 'change' }
        ]
      },
      formLabelWidth: '80px'
    }
  },
  created: function() {
    if (global.state["avatar"] != "super_admin") {
      this.$router.push({path: '/dashboard'});
      this.$message.error('暂无权限访问');
    }
    this.get_form_data()
    this.get_order_form_data()
    this.get_todo_form_data()
    this.get_commission_form_data()
    this.get_private_sea()
    this.addUser(this.pagesize, this.currentPage)
    this.get_group_data()
  },
  methods: {
    submitForm() {
      for (var i = 0, len = this.dynamicValidateForm; i < len; i++) {
        console.log('嘿嘿', this.dynamicValidateForm[i])
      }
      this.axios
        .get('http://127.0.0.1:8000/app/edit_form/', {
          params: {
            // 每页显示的条数
            edit_data: JSON.stringify(this.dynamicValidateForm)
          }
        })
        .then(res => {
          this.$notify({
            title: '提交成功',
            message: '',
            type: 'success'
          })
        })
        .catch(function(error) {
          this.$message({
            type: 'info',
            message: '提交失败'
          })
        })
    },
    addUser(n1, n2) {
      this.axios
        .get('http://127.0.0.1:8000/app/create_user/', {
          params: {
            // 每页显示的条数
            pagesize: n1,
            // 显示第几页
            currentPage: n2
          }
        })
        .then(res => {
          this.tableData = res.data.data
          this.total = res.data.total
          this.loading = false
          console.log(this.tableData)
        })
        .catch(function(error) {
          this.loading = false
          console.log(error)
        })
    },
    order_submitForm() {
      this.axios
        .get('http://127.0.0.1:8000/app/edit_order_form/', {
          params: {
            // 每页显示的条数
            edit_data: JSON.stringify(this.order_dynamicValidateForm)
          }
        })
        .then(res => {
          this.$notify({
            title: '提交成功',
            message: '',
            type: 'success'
          })
          console.log(this.order_dynamicValidateForm)
        })
        .catch(function(error) {
          this.$message({
            type: 'info',
            message: '提交失败'
          })
        })
    },
    todo_submitForm() {
      this.axios
        .get('http://127.0.0.1:8000/app/edit_todo_form/', {
          params: {
            // 每页显示的条数
            edit_data: JSON.stringify(this.to_do_dynamicValidateForm)
          }
        })
        .then(res => {
          this.$notify({
            title: '提交成功',
            message: '',
            type: 'success'
          })
        })
        .catch(function(error) {
          this.$message({
            type: 'info',
            message: '提交失败'
          })
        })
    },
    commission_submitForm() {
      this.axios
        .get('http://127.0.0.1:8000/app/edit_commission_form/', {
          params: {
            // 每页显示的条数
            edit_data: JSON.stringify(this.commission_dynamicValidateForm)
          }
        })
        .then(res => {
          this.$notify({
            title: '提交成功',
            message: '',
            type: 'success'
          })
        })
        .catch(function(error) {
          this.$message({
            type: 'info',
            message: '提交失败'
          })
        })
    },
    get_form_data() {
      this.axios
        .get('http://127.0.0.1:8000/app/get_form/', {})
        .then(res => {
          // this.dynamicValidateForm.push({ label: value,value:"" });
          // this.dynamicValidateForm.push({ label: value,value:"" });
          this.dynamicValidateForm = res.data.data
          console.log(this.dynamicValidateForm)
        })
        .catch(function(error) {
          this.$message({
            type: 'info',
            message: '提交失败'
          })
        })
    },
    get_order_form_data() {
      this.axios
        .get('http://127.0.0.1:8000/app/get_order_form/', {})
        .then(res => {
          // this.dynamicValidateForm.push({ label: value,value:"" });
          // this.dynamicValidateForm.push({ label: value,value:"" });
          this.order_dynamicValidateForm = res.data.data
          console.log(this.order_dynamicValidateForm)
        })
        .catch(function(error) {
          this.$message({
            type: 'info',
            message: '提交失败'
          })
        })
    },
    create_group_name(){
      this.axios
        .get('http://127.0.0.1:8000/app/create_group/', {
          params: {
            // 每页显示的条数
            group_name: this.form.group_name
          }
        })
        .then(res => {
          if(res.data.state == 1){
              this.$notify({
                title: '添加成功',
                message: '',
                type: 'success'
              })
          }else if(res.data.state == 2){
            this.$notify({
                title: '添加失败，销售组已存在',
                message: '',
                type: 'error'
              })
          }

        })
        .catch(function(error) {
          this.$message({
            type: 'info',
            message: '提交失败'
          })
        })
    },
    create_user() {
      this.axios
        .get('http://127.0.0.1:8000/app/create_user_data/', {
          params: {
            // 每页显示的条数
            username: this.form.username,
            first_name: this.form.first_name,
            avatar: this.form.avatar,
            group:this.form.group
          }
        })
        .then(res => {
          this.$notify({
            title: '添加成功',
            message: '',
            type: 'success'
          })
          this.addUser(this.pagesize, this.currentPage)
        })
        .catch(function(error) {
          this.$message({
            type: 'info',
            message: '提交失败'
          })
        })
    },
    update_user(row){
      this.update_user_data.username = row.username
      this.update_user_data.first_name = row.first_name
      this.update_user_data.avatar = row.avatar
      this.update_user_data.group = row.group
    },
    delete_user(row) {
      this.$confirm('确定要将用户删除吗? 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
      .then(() => {
        this.axios
          .get('http://127.0.0.1:8000/app/delete_user/', {
            params: {
              // 每页显示的条数
              username: row.username
            }
          })
          .then(res => {
            this.$notify({
              title: '删除成功',
              message: '',
              type: 'success'
            })
            this.addUser(this.pagesize, this.currentPage)
          })
          .catch(function(error) {
            this.$message({
              type: 'info',
              message: '提交失败'
            })
          })
        })
        .catch(() => {
          this.$notify({
            title: '已取消',
            message: '',
            type: 'info'
          })
        })
    },
    get_todo_form_data() {
      this.axios
        .get('http://127.0.0.1:8000/app/get_todo_form/', {})
        .then(res => {
          // this.dynamicValidateForm.push({ label: value,value:"" });
          // this.dynamicValidateForm.push({ label: value,value:"" });
          this.to_do_dynamicValidateForm = res.data.data
        })
        .catch(function(error) {
          this.$message({
            type: 'info',
            message: '提交失败'
          })
        })
    },
    get_commission_form_data() {
      this.axios
        .get('http://127.0.0.1:8000/app/get_commission_form/', {})
        .then(res => {
          // this.dynamicValidateForm.push({ label: value,value:"" });
          // this.dynamicValidateForm.push({ label: value,value:"" });
          this.commission_dynamicValidateForm = res.data.data
          console.log()
        })
        .catch(function(error) {
          this.$message({
            type: 'info',
            message: '提交失败'
          })
        })
    },
    removeDomain(item) {
      var index = this.dynamicValidateForm.indexOf(item)
      if (index !== -1) {
        this.dynamicValidateForm.splice(index, 1)
      }
    },
    editDomain(item) {
      this.form.name = item.label
      this.form.type = item.type
      this.form.index = item.index
      if (item.type == '选择下拉框') {
        console.log('item.select', item.select)
        this.add_setting = 1
        this.select_Form = item.select
      }
    },
    editForm() {
      var num = ''
      for (var i = 0, len = this.dynamicValidateForm.length; i < len; i++) {
        if (this.form.index == this.dynamicValidateForm[i]['index']) {
          num = i
        }
      }
      this.dynamicValidateForm[num]['label'] = this.form.name
      this.dynamicValidateForm[num]['type'] = this.form.type
      this.$notify({
        title: '修改成功',
        message: '',
        type: 'success'
      })
    },
    addDomain() {
      const name = []
      for (var i = 0, len = this.dynamicValidateForm.length; i < len; i++) {
        name.push(this.dynamicValidateForm[i]['label'])
      }
      if (name.includes(this.form.name) == true) {
        this.$notify({
          title: '添加失败',
          message: '',
          type: 'error'
        })
      } else {
        this.dynamicValidateForm.push({
          label: this.form.name,
          value: '',
          type: this.form.type,
          select: this.select_Form,
          index: this.form.name
        })
        this.$notify({
          title: '添加成功',
          message: '',
          type: 'success'
        })
        console.log(this.dynamicValidateForm)
      }
    },
    selectform() {
      if (this.form.type == '选择下拉框') {
        this.add_setting = 1
      } else {
        this.select_Form = []
        this.add_setting = ''
      }
    },
    order_selectform() {
      if (this.form.order_type == '选择下拉框') {
        this.order_add_setting = 1
      } else {
        this.order_select_Form = []
        this.order_add_setting = ''
      }
    },
    todo_SelectForm() {
      console.log(this.form.select)
      if (this.form.select == '单次任务') {
        this.todo_add_setting2 = 0
        this.todo_add_setting = 1
      } else if (this.form.select == '重复任务') {
        this.todo_add_setting2 = 1
        this.todo_add_setting = 0
      } else {
        this.todo_add_setting = []
        this.todo_add_setting = ''
      }
    },
    get_group_data(){
      this.axios
        .get('http://127.0.0.1:8000/app/get_group_data/')
        .then(res => {
          this.group_data = res.data.data

        })
    },
    update_user_data_yes(){
        this.axios
        .get('http://127.0.0.1:8000/app/update_user_data_yes/', {
          params: {
            // 每页显示的条数
            username:this.update_user_data.username,
            first_name:this.update_user_data.first_name,
            avatar:this.update_user_data.avatar,
            group:this.update_user_data.group,
          }
        })
        .then(res => {
          this.$notify({
                title: '修改成功',
                message: '',
                type: 'success'
          })
          this.addUser(this.pagesize, this.currentPage)
        })
        .catch(function(error) {
          this.loading = false
          console.log(error)
        })
    },
    add_select_form() {
      this.select_Form.push({
        label: this.form.select_text,
        value: this.form.select_text
        // type: ""
      })
      this.form.select_text = ''
    },
    todo_selectform() {
      this.select_Form.push({
        label: this.form.select_text,
        value: this.form.select_text
      })
      this.form.select_text = ''
    },
    order_add_select_form() {
      this.order_select_Form.push({
        label: this.form.order_select_text,
        value: this.form.order_select_text
        // type: ""
      })
      this.form.order_select_text = ''
    },
    select_removeDomain(item) {
      var index = this.select_Form.indexOf(item)
      if (index !== -1) {
        this.select_Form.splice(index, 1)
      }
    },
    order_select_removeDomain(item) {
      var index = this.order_select_Form.indexOf(item)
      if (index !== -1) {
        this.order_select_Form.splice(index, 1)
      }
    },
    todo_select_removeDomain(item, index) {
      // var index = this.todo_select_Form.indexOf(item);
      // if (index !== -1) {
      //   this.todo_select_Form.splice(index, 1);
      // }
      // this.to_do_dynamicValidateForm
      console.log(item, index)
    },
    order_removeDomain(item) {
      var index = this.order_dynamicValidateForm.indexOf(item)
      if (index !== -1) {
        this.order_dynamicValidateForm.splice(index, 1)
      }
    },
    todo_removeDomain(item) {
      var index = this.to_do_dynamicValidateForm.indexOf(item)
      if (index !== -1) {
        this.to_do_dynamicValidateForm.splice(index, 1)
      }
    },
    commission_removeDomain(item) {
      var index = this.commission_dynamicValidateForm.indexOf(item)
      if (index !== -1) {
        this.commission_dynamicValidateForm.splice(index, 1)
      }
    },
    order_editDomain(item) {
      this.form.order_name = item.label
      this.form.order_type = item.type
      this.form.order_index = item.index
      if (item.type == '选择下拉框') {
        this.order_add_setting = 1
        this.order_select_Form = item.select
      }
    },
    todo_editDomain(item) {
      console.log('比阿尼', item)
      this.form.to_do_name = item.name
      this.form.to_do_time = item.time
      this.form.to_do_index = item.index
      this.form.select = item.select
      if (this.form.select == '重复任务') {
        this.todo_add_setting2 = 1
        this.todo_add_setting = 0
      } else {
        this.todo_add_setting = 1
        this.todo_add_setting2 = 0
      }
    },
    commission_editDomain(item) {
      console.log('比阿尼', item)
      this.form.commission_performance = item.commission_performance
      this.form.commission_commission_point = item.commission_commission_point
      this.form.commission_index = item.commission_index
    },
    order_addDomain() {
      // console.log(this.dynamicValidateForm);
      // console.log(this.select_Form);
      const name = []
      for (
        var i = 0, len = this.order_dynamicValidateForm.length;
        i < len;
        i++
      ) {
        name.push(this.order_dynamicValidateForm[i]['label'])
      }
      if (name.includes(this.form.order_name) == true) {
        this.$notify({
          title: '添加失败',
          message: '',
          type: 'error'
        })
      } else {
        this.order_dynamicValidateForm.push({
          label: this.form.order_name,
          value: '',
          type: this.form.order_type,
          select: this.order_select_Form,
          index: this.form.order_name
        })
        this.$notify({
          title: '添加成功',
          message: '',
          type: 'success'
        })
        console.log(this.order_dynamicValidateForm)
      }
    },
    todo_addDomain() {
      const name = []
      for (
        var i = 0, len = this.to_do_dynamicValidateForm.length;
        i < len;
        i++
      ) {
        name.push(this.to_do_dynamicValidateForm[i]['label'])
      }
      if (name.includes(this.form.to_do_name) == true) {
        this.$notify({
          title: '添加失败',
          message: '',
          type: 'error'
        })
      } else {
        this.to_do_dynamicValidateForm.push({
          name: this.form.to_do_name,
          time: this.form.to_do_time,
          index: this.form.to_do_name,
          select: this.form.select
        })
        this.$notify({
          title: '添加成功',
          message: '',
          type: 'success'
        })
        console.log(this.to_do_dynamicValidateForm[i])
      }
    },
    get_private_sea() {
      this.axios
        .get('http://127.0.0.1:8000/app/get_private_sea/', {})
        .then(res => {
          this.private_sea_time = res.data.private_sea_time
          this.private_sea_length = res.data.private_sea_length
        })
        .catch(function(error) {
          this.$message({
            type: 'info',
            message: '提交失败'
          })
        })
    },
    private_sea_edit() {
      this.axios
        .get('http://127.0.0.1:8000/app/private_sea_edit/', {
          params: {
            private_sea_time: this.private_sea_time,
            private_sea_length: this.private_sea_length
          }
        })
        .then(res => {
          this.$notify({
            title: '提交成功',
            message: '',
            type: 'success'
          })
          this.private_sea_time = res.data.private_sea_time
          this.private_sea_length = res.data.private_sea_length
        })
        .catch(function(error) {
          this.$message({
            type: 'info',
            message: '提交失败'
          })
        })
    },
    commission_addDomain() {
      const name = []
      for (
        var i = 0, len = this.commission_dynamicValidateForm.length;
        i < len;
        i++
      ) {
        name.push(
          this.commission_dynamicValidateForm[i]['commission_performance']
        )
      }
      if (name.includes(this.form.to_do_name) == true) {
        this.$notify({
          title: '添加失败',
          message: '',
          type: 'error'
        })
      } else {
        this.commission_dynamicValidateForm.push({
          commission_performance: this.form.commission_performance,
          commission_commission_point: this.form.commission_commission_point,
          commission_index: this.form.commission_performance
        })
        this.$notify({
          title: '添加成功',
          message: '',
          type: 'success'
        })
      }
    },
    order_editForm() {
      var num = ''
      for (
        var i = 0, len = this.order_dynamicValidateForm.length;
        i < len;
        i++
      ) {
        if (
          this.form.order_index == this.order_dynamicValidateForm[i]['index']
        ) {
          num = i
        }
      }
      this.order_dynamicValidateForm[num]['label'] = this.form.order_name
      this.order_dynamicValidateForm[num]['type'] = this.form.order_type
      this.$notify({
        title: '修改成功',
        message: '',
        type: 'success'
      })
    },
    todo_editForm() {
      console.log(this.form.to_do_name)
      console.log(this.form.to_do_time)
      console.log(this.form.select)
      var num = ''
      for (
        var i = 0, len = this.to_do_dynamicValidateForm.length;
        i < len;
        i++
      ) {
        if (
          this.form.to_do_index == this.to_do_dynamicValidateForm[i]['index']
        ) {
          num = i
        }
      }

      this.to_do_dynamicValidateForm[num]['name'] = this.form.to_do_name
      this.to_do_dynamicValidateForm[num]['time'] = this.form.to_do_time
      this.to_do_dynamicValidateForm[num]['select'] = this.form.select
      this.$notify({
        title: '修改成功',
        message: '',
        type: 'success'
      })
    },
    commission_editForm() {
      var num = ''
      for (
        var i = 0, len = this.commission_dynamicValidateForm.length;
        i < len;
        i++
      ) {
        if (
          this.form.commission_index ==
          this.commission_dynamicValidateForm[i]['commission_index']
        ) {
          num = i
        }
      }
      console.log(num)
      this.commission_dynamicValidateForm[num][
        'commission_performance'
      ] = this.form.commission_performance
      this.commission_dynamicValidateForm[num][
        'commission_commission_point'
      ] = this.form.commission_commission_point
      this.$notify({
        title: '修改成功',
        message: '',
        type: 'success'
      })
    },
    handleSizeChange(val) {
      // 改变每页显示的条数
      this.pagesize = val
      // 点击每页显示的条数时，显示第一页
      this.addUser(val, this.currentPage)
      this.qryTableDate()
      // 注意：在改变每页显示的条数时，要将页码显示到第一页
    },
    // 显示第几页
    handleCurrentChange(val) {
      console.log('第几页', val)
      // 改变默认的页数
      this.currentPage = val
      // 切换页码时，要获取每页显示的条数
      this.addUser(this.pagesize, val)
      this.qryTableDate()
    }
  }
}
</script>
