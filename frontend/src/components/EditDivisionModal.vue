<template>
  <el-dialog
    :model-value="localVisible"
    title="Редактировать подразделение"
    width="500px"
    @close="closeModal"
  >
    <el-form :model="localDivision" label-width="120px">
      <el-form-item label="Название">
        <el-input v-model="localDivision.name"></el-input>
      </el-form-item>
      <el-form-item label="Родительское подразделение">
        <el-select v-model="localDivision.parent" placeholder="Выберите подразделение">
          <el-option
            v-for="div in allDivisions"
            :key="div.id"
            :label="div.name"
            :value="div.id"
          />
        </el-select>
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="closeModal">Отмена</el-button>
      <el-button type="primary" @click="saveDivision">Сохранить</el-button>
    </template>
  </el-dialog>
</template>

<script>
export default {
  name: 'EditDivisionModal',
  props: {
    visible: Boolean,
    division: {
      type: Object,
      default: () => ({
        id: null,
        name: '',
        parent: null,
      }),
    },
    allDivisions: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      localVisible: this.visible,
      localDivision: { ...this.division },
    };
  },
  watch: {
    visible(val) {
      this.localVisible = val;
      this.localDivision = { ...this.division };
    },
  },
  methods: {
    closeModal() {
      this.localVisible = false;
      this.$emit('update:visible', false);
    },
    saveDivision() {
      this.$emit('save', { ...this.localDivision });
      this.closeModal();
    },
  },
};
</script>
