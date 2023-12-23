module mem_interface #(
    parameter B_WIDTH = 32;
    parameter MEM_SIZE = 32;
) (
    input                   clk, rst;
    input [B_WIDTH-1:0]     pc;
    input [31:0]            inst;
    input [B_WIDTH-1:0]     mem_addr;
    input                   mem_read_en, mem_write_en;
    input [(B_WIDTH/8)-1:0] write_byte_en;
    inout [B_WIDTH-1:0]     mem_data;
);

    //port connect
    mem_inst #(
       .B_WIDTH(B_WIDTH)
    ) mem_inst (
        .clk(clk), .rst(rst), .pc({'b0,pc[B_WIDTH-2:0]}), .inst(inst)
    );

    mem_data #(
       .B_WIDTH(B_WIDTH)
    ) mem_data (
        .clk(clk), .rst(rst),
        .mem_addr(mem_addr), .mem_data(mem_data),
        .mem_read_en(mem_read_en), .mem_write_en(mem_write_en), .write_byte_en(write_byte_en)
    );


endmodule
