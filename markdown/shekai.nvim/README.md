## Welcome to my theme

### Installation

<details>
  <summary>lazy.nvim</summary>

```lua
{
    "yosskavo/shekai.nvim",
    lazy = false,
    priority = 1000,
    opts = {
        transparent = true, -- Enable background transparency
        blur = true,        -- Enable soft blur background colors
    },
    config = function(_, opts)
        require("shekai").setup(opts)
        vim.cmd("colorscheme shekai")
    end,
}
```
</details>

<details>
  <summary>vim-plug</summary>

```vim
Plug 'Yosskavo/shekai.nvim'
```

```lua
require("shekai").setup({
    transparent = true,
    blur = true,
})
vim.cmd("colorscheme shekai")
```

</details>

### Configuration

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `transparent` | `boolean` | `false` | Enable transparent window backgrounds |
| `blur` | `boolean` | `false` | Enable soft blur dark palette for background and floating panels |

### What is next

- [ ] a theme handler for some main langs (c, c++, py, bash)


