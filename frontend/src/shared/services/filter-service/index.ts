import type { TObjectAny } from "@shared/types/main.types";
import pickBy from "lodash/pickBy";
import { makeAutoObservable } from "mobx";
import qs from "qs";

export class FilterService<TFilters extends TObjectAny> {
  private _filters: Partial<TFilters> = {};

  constructor(private urlPrefix: string = "f") {
    this._filters = this.getFiltersFromURL();

    makeAutoObservable(this);
  }

  // for reactivity
  get filters() {
    return { ...this._filters };
  }

  get hasActiveFilters() {
    return Object.keys(this._filters).length > 0;
  }

  private getFiltersFromURL() {
    const search = window.location.search.substring(1);
    const query = qs.parse(decodeURIComponent(search));

    return (query[this.urlPrefix] || {}) as Partial<TFilters>;
  }

  private updateURL() {
    const search = window.location.search.substring(1);
    const query = qs.parse(search);

    if (Object.keys(this._filters).length === 0) {
      delete query[this.urlPrefix];
    } else {
      query[this.urlPrefix] = this._filters;
    }

    const newSearch = qs.stringify(query, { encode: false });
    const newUrl = `${window.location.pathname}${newSearch ? "?" + newSearch : ""}`;

    window.history.pushState({}, "", newUrl);
  }

  setFilters(newFilters: Partial<TFilters>) {
    this._filters = pickBy(newFilters, Boolean) as Partial<TFilters>;
    this.updateURL();
  }

  setFilter<K extends keyof TFilters>(key: K, value: TFilters[K]) {
    if (value) {
      this._filters[key] = value;
    } else {
      delete this._filters[key];
    }

    this.updateURL();
  }
}
