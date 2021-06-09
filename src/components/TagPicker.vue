<!-- タグ選択ダイアログ -->
<template>
  <div v-show="visible">
    <div class="modal" style="display: block" tabindex="-1">
      <div
        class="
          modal-dialog modal-dialog-centered modal-dialog-scrollable modal-lg
        "
        style="z-index: 2010"
      >
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Select Tags</h5>
          </div>

          <div class="modal-body">
            <div class="container-fluid">
              <div class="row">
                <div class="col-8 overflow-scroll">
                  <!-- 登録済みタグ一覧 -->
                  <div class="list-group" style="height: 50vh">
                    <a
                      v-for="tag in tagFiltered"
                      :key="tag.id"
                      @click="addTag(tag)"
                      class="list-group-item list-group-item-action"
                    >
                      {{ tag.name }}
                    </a>
                  </div>
                </div>

                <div class="col-4">
                  <label>Search</label>
                  <input
                    type="text"
                    class="form-control"
                    v-model="tagFilterKeyword"
                  />
                  <label>Add Tag</label>
                  <input type="text" class="form-control" v-model="newTag" />
                  <button class="form-control btn-primary" @click="createTag">
                    Add
                  </button>
                </div>
              </div>

              <div class="row border-top mt-3 pt-4 mb-2">
                <div class="col-12">
                  <span
                    v-for="tag in tags"
                    :key="tag.id"
                    class="border rounded bg-primary text-white p-2 float-start"
                    >{{ tag.name }}
                    <button
                      class="btn-close btn-close-white"
                      style="font-size: 0.7em"
                      @click="removeTag(tag)"
                    ></button>
                  </span>
                </div>
              </div>
            </div>
          </div>

          <div class="modal-footer">
            <button class="btn btn-primary" @click="close">OK</button>
          </div>
        </div>
      </div>
    </div>

    <div class="modal-backdrop show"></div>
  </div>
</template>

<script lang="ts">
import { Options, Vue } from 'vue-class-component'
import bootstrap from 'bootstrap'
import { dao } from '../dao'
import { Tag } from '../models'
import { consts } from '../consts'

@Options({
  props: {
    tags: {
      type: Array,
      default: []
    },
    visible: {
      type: Boolean,
      default: false
    }
  },
  watch: {
    visible() {
      this.changeVisibility()
    }
  }
})
export default class TagPicker extends Vue {
  tags!: Tag[] // 選択中のタグ一覧
  visible!: boolean

  availableTags: Tag[] = []
  tagFilterKeyword = ''
  newTag = ''

  get tagFiltered(): Tag[] {
    return this.availableTags.filter(tag => tag.name.toLowerCase().includes(this.tagFilterKeyword.toLowerCase()))
  }

  close() {
    this.$emit('close')
  }

  changeVisibility() {
    // 表示時にタグ一覧を取得
    if (this.visible) {
      dao.getTags().then(tags => this.availableTags = tags)
    }
  }

  // タグを追加する
  addTag(tag: Tag): void {
    if (!this.tags.includes(tag)) {
      this.tags.push(tag)
    }
  }

  // タグを選択から削除する
  removeTag(tag: Tag): void {
    let idx = this.tags.indexOf(tag)
    this.tags.splice(idx, 1)
  }

  createTag() {
    const tagname = this.newTag
    const tag = new Tag(null, tagname)
    // タグをDBに登録後、タグ一覧をリクエストして、id を取得する
    // その後、新しく登録したタグを選択状態にする
    dao.createTag(tag)
      .then(res => dao.getTags()
        .then(tags => {
          const tag = tags.find(tag => tag.name == tagname)
          if (tag) {
            this.addTag(tag)
            this.availableTags = tags
          } else {
            console.error('タグ登録失敗')
          }
        })
        .catch(err => console.error(err.result)))
      .catch(err => console.error(err.result))
  }
}
</script>

<style scoped>
</style>