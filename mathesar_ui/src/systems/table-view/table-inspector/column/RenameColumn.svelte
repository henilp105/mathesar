<script lang="ts">
  import EditableTextWithActions from '@mathesar/components/EditableTextWithActions.svelte';
  import type { ColumnsDataStore } from '@mathesar/stores/table-data';
  import type { ProcessedColumn } from '@mathesar/stores/table-data/processedColumns';
  import { toast } from '@mathesar/stores/toast';
  import { getErrorMessage } from '@mathesar/utils/errors';

  export let column: ProcessedColumn;
  export let columnsDataStore: ColumnsDataStore;

  function getValidationErrors(newName: string): string[] {
    if (newName === column.column.name) {
      return [];
    }
    if (!newName) {
      return ['Name cannot be empty.'];
    }
    const columnNames = $columnsDataStore.columns.map((c) => c.name);
    if (columnNames.includes(newName)) {
      return ['A column with that name already exists.'];
    }
    return [];
  }

  async function handleColumnNameChange(newName: string): Promise<void> {
    try {
      await columnsDataStore.rename(column.id, newName);
    } catch (error) {
      toast.error(`Unable to rename column. ${getErrorMessage(error)}`);
    }
  }
</script>

<div class="rename-column-property-container">
  <span class="label">Name</span>
  <EditableTextWithActions
    initialValue={column.column.name}
    onSubmit={handleColumnNameChange}
    {getValidationErrors}
  />
</div>

<style>
  .rename-column-property-container {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }
  .label {
    font-size: var(--text-size-small);
    margin-left: 0.5rem;
  }
</style>
