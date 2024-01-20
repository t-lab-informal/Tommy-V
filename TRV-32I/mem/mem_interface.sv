module mem_interface #(
    parameter B_WIDTH = 32;
    parameter MEM_SIZE = 32;
) (
    input                       clk, rst;
    input  [B_WIDTH-1:0]        pc;
    input  [B_WIDTH-1:0]        mem_addr;
    input                       mem_read_en, mem_write_en;
    input  [(B_WIDTH/8)-1:0]    write_byte_en;
    output [31:0]               inst;
    inout  [B_WIDTH-1:0]        mem_data;
);

    mem_inst #(
       .B_WIDTH(B_WIDTH),
       .MEM_SIZE(MEM_SIZE)
    ) mem_inst (
        .clk(clk), .rst(rst), .pc(pc), .inst(inst)
    );

    mem_data #(
       .B_WIDTH(B_WIDTH),
       .MEM_SIZE(MEM_SIZE)
    ) mem_data (
        .clk(clk), .rst(rst),
        .mem_addr(mem_addr), .mem_data(mem_data),
        .mem_read_en(mem_read_en), .mem_write_en(mem_write_en), .write_byte_en(write_byte_en)
    );


endmodule
