## bot.html documuntation
1. `prev_handler();` it is used to run the code after the `<script>` in base is done.
2. call the `main()` to run the page.
3. in `main()` we run a promise to get all data from the server.
4. after the data is successfuly returned we run `init_blocks_template` passing `options.blockTypes`.
    * `init_blocks_template` is creating blocks templates from all the data returned from server in options.
5. declare `BlockTypes` to be used in dropdown in each block-panel.
6. `render_page` is to render the outer fields.
7. `render_blocks` is the heaviest functin here:
    * if there is not data for this bot show `Sorry there are no blocks for this bot 🙁`
    * if there is a data run a loop `cookUpBlock`
        1. it runs `getTemplate` to init the block
            * it adds placeholders in the panel-body thenn run a checks to remove if it doesn't required to be in the panel-body.
            * in the placeholder replacement we call functions that returns the specific element with a init options.
        2. pass the generated template to be filled by the server data using `getBlockContent`
            * it replaces the placeholders with a pure json data.
    * the `cookUpBlock` function resturns a block with its html data.
    * concatinate it in elements variable.
    * do the same for the rest blocks.
    * finally add the big elements html variable to the `$("#draggablePanelList")`
