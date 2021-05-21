<!-- タグ選択ダイアログ -->
<template>
  <div>
    <div class="modal" tabindex="-1">
      <div
        class="
          modal-dialog modal-dialog-centered modal-dialog-scrollable modal-lg
        "
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
                      @click="onClickRegisterdTag(tag)"
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
                  <input
                    type="text"
                    class="form-control"
                    v-model="tagFilterKeyword"
                  />
                  <button class="form-control btn-primary">Add</button>
                </div>
              </div>

              <div class="row border-top mt-3 pt-4 mb-2">
                <div class="col-12">
                  <span
                    v-for="tag in modelValue"
                    :key="tag.id"
                    class="border rounded bg-primary text-white p-2 float-start"
                    >{{ tag.name }}
                    <button
                      class="btn-close btn-close-white"
                      style="font-size: 0.7em"
                      @click="onClickRemoveTag(tag)"
                    ></button>
                  </span>
                </div>
              </div>
            </div>
          </div>

          <div class="modal-footer">
            <button class="btn btn-primary" data-bs-dismiss="modal">OK</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Options, Vue } from 'vue-class-component'
import bootstrap from 'bootstrap'
import { dao } from '../dao'
import { Tag } from '../model'

@Options({
  props: {
    modelValue: Array
  }
})
export default class TagPicker extends Vue {
  modelValue!: Tag[] // 選択中のタグ一覧

  tags: Tag[] = []
  tagFilterKeyword = ''

  get tagFiltered(): Tag[] {
    return this.tags.filter(tag => tag.name.toLowerCase().includes(this.tagFilterKeyword.toLowerCase()))
  }

  // タグを追加する
  onClickRegisterdTag(tag: Tag): void {
    if (!this.modelValue.includes(tag)) {
      this.modelValue.push(tag)
    }
  }

  // タグを選択から削除する
  onClickRemoveTag(tag: Tag): void {
    let idx = this.modelValue.indexOf(tag)
    this.modelValue.splice(idx, 1)
  }

  mounted(): void {
    // テストデータ
    // sampletags.forEach((tag) => {
    //   this.tagsRegistered.push(tag)
    // })
    dao.getTags()
      .then(tags => { this.tags = tags })
  }
}

let sampletags: string[] = [
  'movie',
  'cinema',
  'music',
  'manga',
  'japan',
  'uk',
  'united states of america',
  'cacao72',
  'furuhata',
  'drama',
  'theksd'
]
</script>

<style scoped>
</style>