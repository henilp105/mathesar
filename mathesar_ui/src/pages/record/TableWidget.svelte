<script lang="ts">
  import type { TableEntry } from '@mathesar/api/tables';
  import type { Column } from '@mathesar/api/tables/columns';
  import { Icon } from '@mathesar/component-library';
  import Identifier from '@mathesar/components/Identifier.svelte';
  import { iconMultipleRecords } from '@mathesar/icons';
  import {
    setTabularDataStoreInContext,
    TabularData,
  } from '@mathesar/stores/table-data/tabularData';
  import TableView from '@mathesar/systems/table-view/TableView.svelte';
  import { currentDbAbstractTypes } from '@mathesar/stores/abstract-types';
  import { Filtering, Meta } from '@mathesar/stores/table-data';
  import Pagination from '@mathesar/utils/Pagination';
  import MiniActionsPane from '@mathesar/systems/table-view/actions-pane/MiniActionsPane.svelte';

  const tabularDataStore = setTabularDataStoreInContext(
    // Sacrifice type safety here since the value is initialized reactively
    // below.
    undefined as unknown as TabularData,
  );

  export let recordId: number;
  export let table: Pick<TableEntry, 'id' | 'name'>;
  export let fkColumn: Pick<Column, 'id' | 'name'>;

  $: meta = new Meta({
    pagination: new Pagination({ size: 10 }),
    filtering: new Filtering({
      combination: 'and',
      entries: [
        { columnId: fkColumn.id, conditionId: 'equal', value: recordId },
      ],
    }),
  });
  $: abstractTypesMap = $currentDbAbstractTypes.data;
  $: tabularData = new TabularData({
    id: table.id,
    abstractTypesMap,
    meta,
  });
  $: tabularDataStore.set(tabularData);
</script>

<div class="table-widget">
  <div class="top">
    <div class="left">
      <Icon {...iconMultipleRecords} size="1.4rem" />
      <h2 class="heading">
        <Identifier>{table.name}</Identifier> Records
      </h2>
      <div class="fk-column">
        (with <Identifier>{fkColumn.name}</Identifier> set to this record)
      </div>
    </div>
    <div class="right">
      <MiniActionsPane />
    </div>
  </div>

  <div class="results">
    <TableView />
  </div>
</div>

<style>
  .top {
    --spacing-x: 1rem;
    --spacing-y: 0.3rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: calc(-1 * var(--spacing-y)) calc(-1 * var(--spacing-x));
    padding-bottom: 1rem;
    flex-wrap: wrap;
  }
  .top > :global(*) {
    margin: var(--spacing-y) var(--spacing-x);
  }
  .left {
    display: grid;
    grid-auto-flow: column;
    gap: 0.5rem;
    align-items: center;
  }
  .heading {
    margin: 0;
  }
  .right {
    flex: 1 0 auto;
    display: flex;
    justify-content: flex-end;
  }
  .fk-column {
    font-size: 1rem;
    font-weight: normal;
    color: var(--color-text-muted);
  }
</style>
