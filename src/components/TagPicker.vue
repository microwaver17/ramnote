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
                      :key="tag"
                      :data-value="tag"
                      @click="onClickRegisterdTag"
                      class="list-group-item list-group-item-action"
                    >
                      {{ tag }}
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
                    :key="tag"
                    class="border rounded bg-primary text-white p-2 float-start"
                    >{{ tag }}
                    <button
                      class="btn-close btn-close-white"
                      style="font-size: 0.7em"
                      :data-value="tag"
                      @click="onClickRemoveTag"
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

@Options({
  props: {
    modelValue: Array
  }
})
export default class TagPicker extends Vue {
  modelValue!: string[] // 選択中のタグ一覧

  tagsRegistered: string[] = []
  tagFilterKeyword = ''

  get tagFiltered(): string[] {
    return this.tagsRegistered.filter(tag => tag.includes(this.tagFilterKeyword))
  }

  // タグを追加する
  onClickRegisterdTag(e: MouseEvent): void {
    let target = e.target as HTMLElement
    let tag = target.dataset.value
    if (tag && !this.modelValue.includes(tag)) {
      this.modelValue.push(tag)
    }
  }

  // タグを選択から削除する
  onClickRemoveTag(e: MouseEvent): void {
    let target = e.target as HTMLElement
    let tag = target.dataset.value
    if (tag && this.modelValue.includes(tag)) {
      let idx = this.modelValue.indexOf(tag)
      this.modelValue.splice(idx)
    }
  }

  mounted(): void {
    // テストデータ
    sampletags.forEach((tag) => {
      this.tagsRegistered.push(tag)
    })
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