<template>
  <li>
    <div :class="['division-item', { selected: isSelected, 'parent-selected': isParentSelected }]" @click="selectDivision">
      <!-- Проверка на наличие дочерних элементов перед отображением иконки -->
      <span v-if="division.children && division.children.length" @click="toggle" class="toggle-icon">
        <img :src="isExpanded ? arrowDown : arrowRight" alt="Toggle" />
      </span>
      <span 
        v-if="!isEditing" 
        @dblclick="enableEdit" 
        @click="selectDivision" 
        class="division-name">
        {{ division.name }}
      </span>
      <input 
        v-else 
        v-model="editName" 
        @blur="saveEdit" 
        @keyup.enter="saveEdit" 
        @keyup.esc="cancelEdit" 
        class="edit-input" 
        type="text" 
      />
      <span @click="confirmDelete(division)" class="delete-icon">✖</span>
    </div>
    <ul v-if="isExpanded && division.children && division.children.length" class="child-list">
      <DivisionItem
        v-for="child in division.children"
        :key="child.id"
        :division="child"
        :selected-id="selectedId"
        :selected-parent-ids="selectedParentIds"
        @update-name="$emit('update-name', $event)"
        @select="$emit('select', $event)" 
        @delete="$emit('delete', $event)" 
      />
    </ul>

    <!-- Модальное окно подтверждения удаления -->
    <el-dialog
      :model-value="showDeleteDialog"
      title="Подтвердить удаление"
      width="400px"
      @close="closeDeleteDialog"
    >
      <span>Вы уверены, что хотите удалить этот элемент?</span>
      <template #footer>
        <el-button @click="closeDeleteDialog">Отмена</el-button>
        <el-button type="primary" @click="deleteItem">Удалить</el-button>
      </template>
    </el-dialog>
  </li>
</template>

<script>
import './Division.css';
import arrowDown from '@/assets/arrow-down.svg';
import arrowRight from '@/assets/arrow-right.svg';

export default {
  name: 'DivisionItem',
  props: {
    division: Object,
    selectedId: Number, // пропс для проверки выделения
    selectedParentIds: { 
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      isExpanded: false,
      isEditing: false,
      editName: this.division.name,
      showDeleteDialog: false,
      itemToDelete: null,
      arrowDown,
      arrowRight,
    };
  },
  computed: {
    isSelected() {
      return this.division.id === this.selectedId; // Проверка, выбран ли текущий элемент
    },
    isParentSelected() {
      return this.selectedParentIds.includes(this.division.id);
    },
  },
  methods: {
    toggle() {
      this.isExpanded = !this.isExpanded;
    },
    enableEdit() {
      this.isEditing = true;
    },
    saveEdit() {
      this.isEditing = false;
      this.$emit('update-name', { id: this.division.id, name: this.editName });
    },
    cancelEdit() {
      this.isEditing = false;
      this.editName = this.division.name;
    },
    selectDivision() {
      this.$emit('select', this.division.id);
    },
    confirmDelete(item) {
      this.itemToDelete = item;
      this.showDeleteDialog = true;
    },
    deleteItem() {
      if (this.itemToDelete) {
        this.$emit('delete', this.itemToDelete.id);
        this.showDeleteDialog = false;
        this.itemToDelete = null;
      }
    },
    closeDeleteDialog() {
      this.showDeleteDialog = false;
      this.itemToDelete = null;
    }
  },
};
</script>
